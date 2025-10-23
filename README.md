# S&P 500 Intraday Data Pipeline

An automated ETL pipeline that extracts, transforms, and loads real-time intraday data for the S&P 500 using Apache Airflow running in Docker.

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Docker Setup](#docker-setup)
  - [Airflow Setup](#airflow-setup)
- [Usage](#usage)
  - [Automation](#automation)
  - [Monitoring](#monitoring)
  - [Data Outputs](#data-outputs)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project leverages Apache Airflow for orchestration and scheduling of an ETL pipeline that processes real-time financial data.

**Workflow Summary:**

- **Extract:** Pulls 1-minute interval data for the top 10 S&P 500 tickers from Yahoo Finance using yfinance.  
- **Transform:** Enhances the dataset with calculated minute returns, trading hours, and additional metrics.  
- **Load:** Pushes the cleaned and transformed data to both Amazon S3 and Snowflake for long-term storage.  

All tasks are automated and executed within Dockerized Airflow containers.

## Technologies Used

| Tool | Purpose |
|------|---------|
| Apache Airflow | Workflow orchestration and scheduling |
| Docker / Docker Compose | Containerization and environment management |
| yfinance | Fetching real-time market data |
| pandas | Data cleaning and transformation |
| Amazon S3 | Cloud data storage |
| Snowflake | Data warehousing and analytics |
| Python 3.x | Primary programming language |

## Prerequisites

- Docker & Docker Compose — [Install Docker](https://docs.docker.com/get-docker/)  
- Python 3.x installed  
- AWS Account — S3 credentials for storage  
- Snowflake Account — Database and warehouse access  
- Git for cloning the repository  

## Setup

### Docker Setup

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
Build and start containers:

bash
Copy code
sudo docker-compose up --build -d
Access Airflow UI: http://localhost:8080

Login credentials:

makefile
Copy code
Username: airflow
Password: airflow
Airflow Setup
Initialize Airflow database:

bash
Copy code
sudo docker-compose run --rm airflow-init
Create connections:

AWS Connection — add your AWS Access Key and Secret Key in the Airflow UI

Snowflake Connection — add your Snowflake credentials (user, password, account, schema)

Schedule the DAG
Airflow automatically executes the ETL DAG as per the configured schedule (@daily or custom).

Usage
Automation
The pipeline runs automatically based on your schedule

Each step — Extract, Transform, Load — is fully monitored via the Airflow UI

Monitoring
Track task success/failure

View detailed logs

Trigger manual runs if needed

Data Outputs
Amazon S3:

arduino
Copy code
s3://your-bucket/sp500_intraday/{trading_date}.csv
Snowflake:
Data loaded into Snowflake tables for further analysis.

Contributing
Fork the repository

Create a feature branch:

bash
Copy code
git checkout -b feature-name
Commit your changes:

bash
Copy code
git commit -am "Add new feature"
Push your branch:

bash
Copy code
git push origin feature-name
Open a Pull Request to merge into main

License
Licensed under the MIT License. See the LICENSE.txt file for full details.
