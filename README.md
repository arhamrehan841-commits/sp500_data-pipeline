🌐 S&P 500 Intraday Data Pipeline 🚀

An automated ETL pipeline that extracts, transforms, and loads real-time intraday data for the S&P 500 using Apache Airflow running in Docker.

The pipeline fetches 1-minute interval stock data from Yahoo Finance, processes it for advanced analytics, and seamlessly loads it into Amazon S3 and Snowflake for storage and visualization. 📈❄️

📋 Table of Contents

📖 Project Overview

⚙️ Technologies Used

📝 Prerequisites

🔧 Setup

🐳 Docker Setup

🛠️ Airflow Setup

🚀 Usage

💡 Contributing

📜 License

📖 Project Overview

This project leverages Apache Airflow for orchestration and scheduling of an ETL pipeline that processes real-time financial data.

Workflow Summary:

Extract → Pulls 1-minute interval data for the top 10 S&P 500 tickers from Yahoo Finance using yfinance.

Transform → Enhances the dataset with calculated minute returns, trading hours, and additional metrics for analysis.

Load → Pushes the cleaned, transformed data to both Amazon S3 and Snowflake for long-term storage and querying.

All tasks are automated and executed within Dockerized Airflow containers, ensuring a reproducible and isolated environment. 🧩

⚙️ Technologies Used
Tool	Purpose
🐳 Apache Airflow	Workflow orchestration and scheduling
🐋 Docker / Docker Compose	Containerization and environment management
📊 yfinance	Fetching real-time market data
🧹 pandas	Data cleaning and transformation
☁️ Amazon S3	Cloud data storage
❄️ Snowflake	Data warehousing and analytics
🐍 Python 3.x	Primary programming language
📝 Prerequisites

Before setup, ensure you have:

✅ Docker & Docker Compose → Install Docker

✅ Python 3.x installed
✅ AWS Account → S3 credentials for storage
✅ Snowflake Account → Database and warehouse access
✅ Git for cloning the repository

🔧 Setup
🐳 Docker Setup

1️⃣ Clone the Repository

git clone <repository_url>
cd <repository_directory>


2️⃣ Build and Start Containers

sudo docker-compose up --build -d


3️⃣ Access Airflow UI
Open: 👉 http://localhost:8080

Login Credentials:

Username: airflow
Password: airflow

🛠️ Airflow Setup

1️⃣ Initialize Airflow Database

sudo docker-compose run --rm airflow-init


2️⃣ Create Connections

AWS Connection → Add your AWS Access Key & Secret Key in the Airflow UI

Snowflake Connection → Add your Snowflake credentials (user, password, account, schema)

3️⃣ Schedule the DAG
Airflow will automatically schedule and execute the ETL DAG as per its defined frequency (@daily, or as configured).

🚀 Usage

Once deployed, your Airflow DAG (sp500_intraday_dag.py) automates the full ETL process.

🔁 Automation

The pipeline runs automatically based on your chosen schedule.

Each step — Extract, Transform, Load — is fully monitored via the Airflow UI.

📊 Monitoring

In the Airflow UI, you can:

✅ Track task success/failure

📜 View detailed logs

🔁 Trigger manual runs as needed

📦 Data Outputs

Amazon S3:
Processed data stored under

s3://your-bucket/sp500_intraday/{trading_date}.csv


Snowflake:
Data loaded into Snowflake tables for advanced analysis and dashboarding.

💡 Contributing

We welcome all contributions! 🧠

Fork the repository

Create a feature branch

git checkout -b feature-name


Commit your changes

git commit -am "Add new feature"


Push your branch

git push origin feature-name


Open a Pull Request to merge your changes into main

📜 License

Licensed under the MIT License.
See the LICENSE
 file for full details.

💬 Made with 💻 + 📈 to automate the future of financial data.
