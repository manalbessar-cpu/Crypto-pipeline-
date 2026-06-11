from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

# =========================
# DEFAULT SETTINGS
# =========================
default_args = {
    "owner": "manal",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# =========================
# FUNCTIONS (replace with your scripts)
# =========================

def ingest_bronze():
    print("📥 Ingesting raw data to Bronze layer...")

def transform_silver():
    print("⚙️ Transforming data to Silver layer...")

def build_gold_model():
    print("🏗 Building Gold data model (parquet files)...")

def load_snowflake():
    print("🚀 Loading data into Snowflake...")
    os.system("python src/snowflake/load_snowflake.py")


# =========================
# DAG DEFINITION
# =========================
with DAG(
    dag_id="cryptopipelinedag",
    default_args=default_args,
    description="Crypto End-to-End Pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",   # ⏰ daily run
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id="ingest_bronze",
        python_callable=ingest_bronze
    )

    task2 = PythonOperator(
        task_id="transform_silver",
        python_callable=transform_silver
    )

    task3 = PythonOperator(
        task_id="build_gold_model",
        python_callable=build_gold_model
    )

    task4 = PythonOperator(
        task_id="load_snowflake",
        python_callable=load_snowflake
    )

    # =========================
    # PIPELINE FLOW
    # =========================
    task1 >> task2 >> task3 >> task4