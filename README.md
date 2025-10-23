markdown# S&P 500 Intraday Data Pipeline

An automated ETL pipeline that extracts, transforms, and loads **real-time intraday data** for the S&P 500 using **Apache Airflow** running in **Docker**.

The pipeline fetches **1-minute interval** stock data from **Yahoo Finance**, processes it for advanced analytics, and loads it into **Amazon S3** and **Snowflake** for storage and visualization.

---

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

---

## Project Overview

This project leverages [**Apache Airflow**](https://airflow.apache.org/) for orchestrating and scheduling an ETL pipeline that processes real-time financial data.

### Workflow Summary
| Stage     | Action                                                                 |
|---------|------------------------------------------------------------------------|
| **Extract**  | Pulls 1-minute interval data for the **top 10 S&P 500 tickers** from [Yahoo Finance](https://finance.yahoo.com/) using [`yfinance`](https://github.com/ranaroussi/yfinance) |
| **Transform**| Calculates minute returns, filters trading hours, adds technical indicators |
| **Load**     | Stores transformed data in [**Amazon S3**](https://aws.amazon.com/s3/) and [**Snowflake**](https://www.snowflake.com/) |

All tasks run in **Dockerized Airflow containers**, ensuring reproducibility and isolation.

---

## Technologies Used

| Tool | Purpose |
|------|---------|
| [**Apache Airflow**](https://airflow.apache.org/) | Workflow orchestration & scheduling |
| [**Docker**](https://www.docker.com/) / [**Docker Compose**](https://docs.docker.com/compose/) | Containerization & environment management |
| [**yfinance**](https://github.com/ranaroussi/yfinance) | Real-time market data extraction |
| [**pandas**](https://pandas.pydata.org/) | Data transformation & cleaning |
| [**Amazon S3**](https://aws.amazon.com/s3/) | Scalable cloud object storage |
| [**Snowflake**](https://www.snowflake.com/) | Cloud data warehouse for analytics |
| [**Python 3.x**](https://www.python.org/) | Core programming language |

---

## Prerequisites

Ensure the following are installed and configured:

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.x](https://www.python.org/downloads/)
- [AWS Account](https://aws.amazon.com/) with S3 bucket and IAM credentials
- [Snowflake Account](https://www.snowflake.com/) with database, schema, and warehouse
- [Git](https://git-scm.com/) for cloning the repository

---

## Setup

### Docker Setup

```bash
git clone <repository_url>
cd <repository_directory>
Build and start services in detached mode:
bashsudo docker-compose up --build -d
Access the Airflow Web UI:
http://localhost:8080
Default Login

Username: airflow
Password: airflow

Airflow Setup
Initialize the Airflow metadata database:
bashsudo docker-compose run --rm airflow-init
Configure Connections in Airflow UI

AWS S3 Connection

Conn ID: aws_default
Access Key ID & Secret Access Key


Snowflake Connection

Conn ID: snowflake_default
Account, User, Password, Database, Schema, Warehouse



The ETL DAG runs automatically on the defined schedule (@daily or custom).

Usage
Automation

Pipeline executes automatically per schedule
All tasks (Extract → Transform → Load) are fully traceable

Monitoring
Use the Airflow UI at http://localhost:8080 to:

Monitor task status (success/failure)
View real-time logs
Trigger manual DAG runs
Set up alerts and retries


Data Outputs
Amazon S3
texts3://your-bucket/sp500_intraday/{trading_date}.csv

Partitioned by trading date for efficient querying.

Snowflake
Data loaded into:
sqlDATABASE.SP500_SCHEMA.INTRADAY_DATA
Ready for BI tools (Tableau, Power BI) and SQL analytics.

Contributing
We welcome contributions!

Fork the repository
Create a feature branch:
bashgit checkout -b feature/your-feature-name

Commit your changes:
bashgit commit -m "Add: your feature description"

Push and open a Pull Request:
bashgit push origin feature/your-feature-name



License
This project is licensed under the MIT License.
See the LICENSE.txt file for full details.


  Made with code + data to automate the future of financial analytics.

```
