S&P 500 Intraday Data Pipeline
An automated ETL pipeline that extracts, transforms, and loads real-time intraday data for the S&P 500 using Apache Airflow running in Docker. The pipeline fetches 1-minute interval stock data from Yahoo Finance, processes it for advanced analytics, and loads it into Amazon S3 and Snowflake for storage and visualization.
Table of Contents

Project Overview
Technologies Used
Prerequisites
Setup
Docker Setup
Airflow Setup


Usage
Automation
Monitoring


Data Outputs
Contributing
License

Project Overview
This project leverages Apache Airflow for orchestrating and scheduling an ETL pipeline that processes real-time financial data.
Workflow Summary:

Extract: Pulls 1-minute interval data for the top 10 S&P 500 tickers from Yahoo Finance using yfinance.
Transform: Enhances the dataset with calculated minute returns, trading hours, and additional metrics for analysis.
Load: Pushes the cleaned and transformed data to both Amazon S3 and Snowflake for long-term storage.

All tasks are automated and executed within Dockerized Airflow containers, ensuring a reproducible and isolated environment.
Technologies Used



Tool
Purpose



Apache Airflow
Workflow orchestration and scheduling


Docker / Docker Compose
Containerization and environment management


yfinance
Fetching real-time market data


pandas
Data cleaning and transformation


Amazon S3
Cloud data storage


Snowflake
Data warehousing and analytics


Python 3.x
Primary programming language


Prerequisites
Before setup, ensure you have:

Docker & Docker Compose installed
Python 3.x installed
AWS Account with S3 credentials for storage
Snowflake Account with database and warehouse access
Git for cloning the repository

Setup
Docker Setup

Clone the repository:
git clone <repository_url>
cd <repository_directory>


Build and start containers:
sudo docker-compose up --build -d


Access the Airflow UI at http://localhost:8080.

Login credentials:
Username: airflow
Password: airflow





Airflow Setup

Initialize the Airflow database:
sudo docker-compose run --rm airflow-init


Create connections in the Airflow UI:

AWS Connection: Add AWS Access Key & Secret Key
Snowflake Connection: Add your Snowflake credentials (user, password, account, schema)


Schedule the DAG:

Airflow automatically executes the ETL DAG based on the configured schedule (@daily or custom).



Usage
Automation

The pipeline runs automatically based on your configured schedule.
Each step—Extract, Transform, Load—is fully monitored via the Airflow UI.

Monitoring
In the Airflow UI, you can:

Track task success/failure
View detailed logs
Trigger manual runs if needed

Data Outputs

Amazon S3:

Processed data stored under:s3://your-bucket/sp500_intraday/{trading_date}.csv




Snowflake:

Data loaded into Snowflake tables for further analysis.



Contributing
We welcome contributions! Follow these steps:

Fork the repository.
Create a feature branch:git checkout -b feature-name


Commit your changes:git commit -am "Add new feature"


Push your branch:git push origin feature-name


Open a Pull Request to merge into main.

License
Licensed under the MIT License. See the LICENSE.txt file for full details.

💬 Made with code + data to automate the future of financial data.
