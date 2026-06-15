from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator


# -----------------------------
# TASK 1: BRONZE INGESTION
# -----------------------------
def ingest_bronze():
    print("🥉 Ingesting data from API (Bronze layer)")


# -----------------------------
# TASK 2: SILVER TRANSFORM
# -----------------------------
def transform_silver():
    print("🥈 Cleaning & transforming data (Silver layer)")


# -----------------------------
# TASK 3: GOLD MODEL
# -----------------------------
def build_gold_model():
    print("🥇 Building analytics model (Gold layer)")


# -----------------------------
# TASK 4: LOAD TO SNOWFLAKE
# -----------------------------
def load_snowflake():
    print("❄ Loading data into Snowflake warehouse")


# -----------------------------
# DEFAULT CONFIG
# -----------------------------
default_args = {
    "owner": "manal",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
    "email_on_failure": True,
}

# -----------------------------
# DAG DEFINITION
# -----------------------------
with DAG(
    dag_id="cryptopipelinedag",
    description="Crypto pipeline Bronze → Silver → Gold → Snowflake",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
) as dag:

    t1 = PythonOperator(
        task_id="ingestbronze",
        python_callable=ingest_bronze,
    )

    t2 = PythonOperator(
        task_id="transformsilver",
        python_callable=transform_silver,
    )

    t3 = PythonOperator(
        task_id="buildgoldmodel",
        python_callable=build_gold_model,
    )

    t4 = PythonOperator(
        task_id="load_snowflake",
        python_callable=load_snowflake,
    )

    # PIPELINE ORDER
    t1 >> t2 >> t3 >> t4