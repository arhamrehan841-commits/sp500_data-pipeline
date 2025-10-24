-- ================================================================
-- Project  : S&P 500 ETL Pipeline (Apache Airflow)
-- Database : Snowflake
-- File     : 01_create_sp500_table.sql
-- Purpose  : Create table to store 1-minute intraday S&P 500 data
-- Author   : [Your Name]
-- Created  : [Date]
-- ================================================================


-- ================================================================
-- Step 1: Create and use project database
-- ================================================================
CREATE DATABASE IF NOT EXISTS AIRFLOW_PROJECT;

USE DATABASE AIRFLOW_PROJECT;


-- ================================================================
-- Step 2: Create schema (optional but good practice)
-- ================================================================
CREATE SCHEMA IF NOT EXISTS PUBLIC;


-- ================================================================
-- Step 3: Create table for S&P 500 intraday data
-- ================================================================
CREATE OR REPLACE TABLE AIRFLOW_PROJECT.PUBLIC.SP500_DATA_PER_MINUTE (
    EVENT_TIMESTAMP TIMESTAMP_NTZ(9) NOT NULL,       -- Exact timestamp of trade
    TRADING_DATE DATE NOT NULL,                      -- Trading date (YYYY-MM-DD)
    TICKER VARCHAR(10) NOT NULL,                     -- Stock symbol (e.g., AAPL, MSFT)
    OPEN FLOAT,                                      -- Opening price for the minute
    HIGH FLOAT,                                      -- Highest price in that minute
    LOW FLOAT,                                       -- Lowest price in that minute
    CLOSE FLOAT,                                     -- Closing price for the minute
    VOLUME NUMBER(38,0),                             -- Total volume traded in that minute
    MINUTE_RETURN FLOAT,                             -- Return computed per minute
    TRADE_HOUR NUMBER(38,0),                         -- Hour of trade (for time grouping)
    TRADE_MINUTE NUMBER(38,0),                       -- Minute of trade
    LOADED_AT TIMESTAMP_LTZ(9) DEFAULT CURRENT_TIMESTAMP(), -- Load timestamp (ETL insert time)
    
    PRIMARY KEY (EVENT_TIMESTAMP, TICKER)            -- Composite primary key
);


-- ================================================================
-- Step 4: Verify the table creation
-- ================================================================
SELECT * 
FROM AIRFLOW_PROJECT.PUBLIC.SP500_DATA_PER_MINUTE
LIMIT 10;
