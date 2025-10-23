from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging

# Import your ETL functions
from sp500_pipeline import run_etl_pipeline  # Replace 'your_module' with actual module name

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
with DAG(
    dag_id='sp500_intraday_daily',
    default_args=default_args,
    description='Daily ETL DAG for S&P 500 intraday data',
    schedule_interval='0 6 * * *',  # Run daily at 6 AM
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['sp500', 'intraday'],
) as dag:

    # PythonOperator to run ETL
    etl_task = PythonOperator(
        task_id='run_intraday_etl',
        python_callable=run_etl_pipeline
    )

    etl_task