import yfinance as yf
import pandas as pd
import time
import logging
from datetime import datetime, timedelta
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from typing import List, Dict
from io import StringIO

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample S&P 500 tickers
SP500_TOP_10 = [
    "NVDA", "MSFT", "AAPL", "AMZN", "META", "AVGO", "GOOGL", "GOOG", "BRK.B", "TSLA",
    "JPM", "V", "LLY", "NFLX", "MA", "COST", "XOM", "WMT", "PG", "JNJ",
    "UNH", "HD", "BAC", "DIS", "KO", "PFE", "MRK", "CSCO", "ADBE", "CRM",
    "ORCL", "ABT", "TXN", "CMCSA", "NEE", "NFLX", "T", "INTC", "NKE", "WBA",
    "MCD", "AMD", "PYPL", "BA", "PEP", "LLY", "ZM", "QCOM", "LMT", "CVX"
]

# US Market Holidays 2025
US_HOLIDAYS_2025 = {
    "2025-01-01", "2025-01-20", "2025-02-17", "2025-04-18",
    "2025-05-26", "2025-06-19", "2025-07-04", "2025-09-01",
    "2025-11-27", "2025-12-25"
}

# Check if a given date is a weekend
def is_weekend(date_obj: datetime) -> bool:
    return date_obj.weekday() >= 5

# Check if a given date is a market holiday
def is_market_holiday(date_obj: datetime) -> bool:
    return date_obj.strftime("%Y-%m-%d") in US_HOLIDAYS_2025

# Get the last N trading days (excluding weekends and holidays)
def get_last_n_trading_days(n: int) -> List[str]:
    trading_days = []
    current_date = datetime.now() - timedelta(days=1)  # Start from yesterday
    while len(trading_days) < n:
        if not is_weekend(current_date) and not is_market_holiday(current_date):
            trading_days.append(current_date.strftime("%Y-%m-%d"))
        current_date -= timedelta(days=1)
    trading_days.reverse()  # Oldest first
    return trading_days[0]

# Validate the downloaded data for a ticker
def validate_ticker_data(df: pd.DataFrame, ticker: str) -> bool:
    if df.empty:
        logger.warning(f"Empty DataFrame for {ticker}")
        return False

    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        logger.warning(f"Missing columns for {ticker}: {missing_cols}")
        return False

    critical_nulls = all(df[col].isna().all() for col in ['Open', 'Close'])
    if critical_nulls:
        logger.warning(f"All critical price data is NaN for {ticker}")
        return False

    return True

# Extract intraday data for tickers
def extract_intraday_data(tickers: List[str], trading_date: str, retry_attempts: int = 2) -> Dict[str, List[dict]]:
    logger.info(f"Starting intraday extraction for {len(tickers)} tickers on {trading_date}")
    historical_data = {}
    failed_tickers = []

    start_date = trading_date
    end_date = (datetime.strptime(trading_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

    logger.info(f"Date range: {start_date} to {end_date}")

    for idx, ticker in enumerate(tickers, 1):
        success = False
        logger.info(f"[{idx}/{len(tickers)}] Processing {ticker}...")

        for attempt in range(retry_attempts):
            try:
                logger.info(f"  Downloading {ticker} 1-minute data (attempt {attempt + 1}/{retry_attempts})")
                df = yf.download(ticker, interval="1m", start=start_date, end=end_date, prepost=False, threads=False)
                df.columns = df.columns.get_level_values(0)    
                df = df.rename(columns=str.lower)

                if validate_ticker_data(df, ticker):
                    records = [
                        {
                            'timestamp': ts,
                            'trading_date': trading_date,
                            'ticker': ticker,
                            'open': float(r['open']) if pd.notna(r['open']) else 0.0,
                            'high': float(r['high']) if pd.notna(r['high']) else 0.0,
                            'low': float(r['low']) if pd.notna(r['low']) else 0.0,
                            'close': float(r['close']) if pd.notna(r['close']) else 0.0,
                            'volume': int(r['volume']) if pd.notna(r['volume']) else 0
                        }
                        for ts, r in df.iterrows()
                    ]
                    historical_data[ticker] = records
                    logger.info(f"  ✓ Successfully downloaded {ticker}: {len(records)} minute bars")
                    success = True
                    break
                else:
                    logger.warning(f"  ✗ Invalid data for {ticker}")

            except Exception as e:
                logger.error(f"  ✗ Error downloading {ticker} (attempt {attempt + 1}): {e}")
                if attempt < retry_attempts - 1:
                    time.sleep(2)

        if not success:
            failed_tickers.append(ticker)
            logger.error(f"  ✗ Failed to download {ticker} after {retry_attempts} attempts")

        time.sleep(1)

    success_count = len(historical_data)
    failure_count = len(failed_tickers)
    total_rows = sum(len(records) for records in historical_data.values())

    logger.info(f"\n{'='*80}")
    logger.info("EXTRACTION SUMMARY")
    logger.info(f"{'='*80}")
    logger.info(f"Successful: {success_count}/{len(tickers)} tickers")
    logger.info(f"Failed: {failure_count}/{len(tickers)} tickers")
    logger.info(f"Total minute bars: {total_rows:,}")

    if failed_tickers:
        logger.warning(f"Failed tickers: {', '.join(failed_tickers)}")

    if not historical_data:
        raise ValueError("Extraction failed for all tickers. Aborting pipeline.")

    return historical_data

# Transform extracted data
def transform_intraday_data(historical_data: Dict[str, List[dict]], trading_date: str):
    if not historical_data:
        logger.warning("No data received to transform.")
        return None

    logger.info(f"\n{'='*80}")
    logger.info(f"TRANSFORMATION PHASE")
    logger.info(f"{'='*80}")
    logger.info(f"Transforming data for {len(historical_data)} tickers...")

    transformed_data = {}

    for ticker, records in historical_data.items():
        if not records:
            logger.warning(f"No records found for {ticker}")
            continue

        df = pd.DataFrame(records)
        if df.empty:
            logger.warning(f"{ticker} returned an empty DataFrame")
            continue

        df.rename(columns={'timestamp': 'event_timestamp'}, inplace=True)
        df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])
        df = df.sort_values('event_timestamp')
        df['minute_return'] = df['close'].pct_change(fill_method=None) * 100
        df['minute_return'] = df['minute_return'].fillna(0)
        df['trade_hour'] = df['event_timestamp'].dt.hour
        df['trade_minute'] = df['event_timestamp'].dt.minute
        df['trading_date'] = trading_date
        df['ticker'] = ticker

        df = df[['event_timestamp', 'trading_date', 'ticker', 'open', 'high', 'low', 'close',
                 'volume', 'minute_return', 'trade_hour', 'trade_minute']]

        transformed_data[ticker] = df
        logger.info(f"✓ Transformed {ticker}: {len(df)} records")

    logger.info(f"\n{'='*80}")
    logger.info(f"TRANSFORMATION SUMMARY")
    logger.info(f"{'='*80}")
    logger.info(f"Tickers transformed: {len(transformed_data)}")

    return transformed_data

# Load data to S3
def load_to_s3(a_df: pd.DataFrame, trading_date: str, bucket: str = "airflow-project-smit") -> None:
    try:
        logger.info(f"\n{'='*80}")
        logger.info(f"LOADING TO S3")
        logger.info(f"{'='*80}")

        s3_hook = S3Hook(aws_conn_id='aws_default')
        
        df = pd.concat(a_df.values(), ignore_index=True) 
        
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        daily_key = f"sp500_intraday/{trading_date}.csv"
        logger.info(f"Uploading to s3://{bucket}/{daily_key}")
        logger.info(f"File size: {len(csv_data) / 1024 / 1024:.2f} MB")

        s3_hook.load_string(
            string_data=csv_data,
            key=daily_key,
            bucket_name=bucket,
            replace=True
        )
        logger.info(f"✓ Successfully uploaded daily file")

        latest_key = "sp500_intraday/latest.csv"
        s3_hook.load_string(
            string_data=csv_data,
            key=latest_key,
            bucket_name=bucket,
            replace=True
        )
        logger.info(f"✓ Updated latest file")

    except Exception as e:
        logger.error(f"✗ Failed to load to S3: {str(e)}")
        raise

# Load data to Snowflake
def load_to_snowflake(s_df: pd.DataFrame, trading_date ,table: str = "SP500_DATA_PER_MINUTE") -> None:
    try:
        logger.info(f"\n{'='*80}")
        logger.info(f"LOADING TO SNOWFLAKE")
        logger.info(f"{'='*80}")
        
        df = pd.concat(s_df.values(), ignore_index=True)
        
        snowflake_hook = SnowflakeHook(snowflake_conn_id='snowflake_default')

        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table} (
            event_timestamp TIMESTAMP_NTZ NOT NULL,
            trading_date DATE NOT NULL,
            ticker VARCHAR(10) NOT NULL,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            volume BIGINT,
            minute_return FLOAT,
            trade_hour INT,
            trade_minute INT,
            loaded_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
            PRIMARY KEY (event_timestamp, ticker)
        )
        """
        logger.info(f"Ensuring table {table} exists...")
        snowflake_hook.run(create_table_sql)

        rows = []
        for _, row in df.iterrows():
            rows.append((row['event_timestamp'], row['trading_date'], row['ticker'],
                         float(row['open']), float(row['high']), float(row['low']), float(row['close']),
                         int(row['volume']), float(row['minute_return']), int(row['trade_hour']),
                         int(row['trade_minute'])))

        batch_size = 1000
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            snowflake_hook.insert_rows(
                table=table,
                rows=batch,
                target_fields=['event_timestamp', 'trading_date', 'ticker', 'open', 'high', 'low', 'close',
                               'volume', 'minute_return', 'trade_hour', 'trade_minute']
            )
            logger.info(f"  Inserted batch {i//batch_size + 1}/{(len(rows)-1)//batch_size + 1}")

        logger.info(f"✓ Successfully loaded {len(rows):,} records")

        verify_sql = f"SELECT COUNT(*) as cnt FROM {table} WHERE trading_date = '{trading_date}'"
        result = snowflake_hook.get_first(verify_sql)
        logger.info(f"Verification: {result[0]:,} records in Snowflake for {trading_date}")

    except Exception as e:
        logger.error(f"✗ Failed to load to Snowflake: {str(e)}")
        raise

# Main ETL function
def run_etl_pipeline():
    try:
        tickers = SP500_TOP_10
        trading_date = get_last_n_trading_days(n=1)

        logger.info(f"\n{'='*80}")
        logger.info(f"S&P 500 INTRADAY DATA PIPELINE")
        logger.info(f"{'='*80}")
        logger.info(f"Trading Date: {trading_date}")
        logger.info(f"Tickers: {len(tickers)}")
        logger.info(f"Data Type: 1-minute intervals")
        logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"{'='*80}\n")

        historical_data = extract_intraday_data(tickers, trading_date)
        transformed_df = transform_intraday_data(historical_data, trading_date)

        if transformed_df is None:
            logger.error("No data to load. Pipeline aborted.")
            return

        load_to_s3(transformed_df, trading_date)
        load_to_snowflake(transformed_df, trading_date)

        logger.info(f"\n{'='*80}")
        logger.info(f"PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info(f"{'='*80}")
        logger.info(f"Trading Date: {trading_date}")
        logger.info(f"Total Records: {len(transformed_df):,}")
        logger.info(f"Unique Tickers: {transformed_df['ticker'].nunique()}")
        logger.info(f"Time Range: {transformed_df['timestamp'].min()} to {transformed_df['timestamp'].max()}")
        logger.info(f"Total Volume: {transformed_df['volume'].sum():,}")
        logger.info(f"Avg Close Price: ${transformed_df['close'].mean():.2f}")
        logger.info(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"{'='*80}\n")

    except Exception as e:
        logger.error(f"\n{'='*80}")
        logger.error(f"PIPELINE FAILED!")
        logger.error(f"{'='*80}")
        logger.error(f"Error: {str(e)}", exc_info=True)
        logger.error(f"{'='*80}\n")
        raise

if __name__ == "__main__":
    test_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA']
    logger.info("Running in TEST MODE with 5 tickers")
    run_etl_pipeline(tickers=test_tickers)
