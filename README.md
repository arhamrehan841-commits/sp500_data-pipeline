🌐 S&P 500 Intraday Data Pipeline 🚀

This project automates the extraction, transformation, and loading (ETL) of S&P 500 intraday data using Airflow running in Docker. The pipeline fetches real-time 1-minute interval data from Yahoo Finance, processes it, and uploads it to Amazon S3 and Snowflake for further analysis. 📈📊

📋 Table of Contents

Project Overview

Technologies Used

Prerequisites

Setup

Docker Setup

Airflow Setup

Usage

Contributing

License

📖 Project Overview

This project leverages Apache Airflow for scheduling and orchestrating an ETL pipeline that fetches 1-minute interval data for top S&P 500 stocks from Yahoo Finance.

Extract: Fetches data for the top 10 S&P 500 tickers using yfinance.

Transform: Processes the data by adding minute returns, trading hour, and other useful metrics.

Load: Uploads the cleaned and transformed data to Amazon S3 and Snowflake.

Automated workflows are managed by Apache Airflow and run within Docker containers for an isolated and reproducible environment. 🛠️

⚙️ Technologies Used

Apache Airflow 🐳 (workflow orchestration)

Docker 🐋 (containerization)

yfinance 📊 (financial data retrieval)

pandas 🧹 (data processing)

Amazon S3 ☁️ (data storage)

Snowflake ❄️ (data warehousing)

Python 🐍 (primary programming language)

Docker Compose 📦 (manages multi-container Docker applications)

📝 Prerequisites

Before setting up the project, ensure that you have the following:

Docker and Docker Compose: Follow the installation guide
 to install Docker on your system.

Python 3.x: Ensure Python is installed on your system.

AWS account: You will need AWS credentials (S3 access).

Snowflake account: For loading the data into Snowflake.

Git: To clone the repository.

🔧 Setup
Docker Setup 🐳

Install Docker:

Follow the Docker installation guide
 to install Docker on your system.

Clone the Repository:

git clone <repository_url>
cd <repository_directory>


Build and Start the Docker Containers:
Use Docker Compose to set up the Airflow, PostgreSQL, Redis, and other services:

sudo docker-compose up --build -d


Access the Airflow Web UI:
After the containers are up, visit http://localhost:8080
 to access the Airflow UI. The default login credentials are:

Username: airflow

Password: airflow

Airflow Setup 🛠️

Initialize the Airflow Database:

sudo docker-compose run --rm airflow-init


Create Connections:

AWS Connection: Add AWS credentials (access key and secret key) in the Airflow UI.

Snowflake Connection: Provide your Snowflake credentials in the Airflow UI.

Schedule the DAG:
Airflow will automatically schedule and run the ETL DAG based on the defined schedule (e.g., @daily).

🚀 Usage
Automate the ETL Pipeline

Scheduling: The ETL pipeline will automatically run based on the schedule you set in the Airflow UI (or within the DAG file itself).

Monitoring: Monitor the ETL pipeline in real-time via the Airflow UI:

View task logs 📝

Check task status (success, failure, retries) ✅❌

Data Outputs:

The processed data will be available in Amazon S3 under the folder sp500_intraday/{trading_date}.csv.

Data will also be uploaded to Snowflake for further analysis.

Example of running the pipeline:

The sp500_intraday_dag.py file orchestrates the pipeline. After the setup, this DAG will automatically trigger to extract, transform, and load the S&P 500 data.

💡 Contributing

We welcome contributions to improve this project! To contribute:

Fork the repository.

Create a new branch (git checkout -b feature-name).

Commit your changes (git commit -am 'Add new feature').

Push your branch (git push origin feature-name).

Open a pull request to merge your changes into the main branch.

📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.
