import datetime
import sys
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

sys.path.append("/opt/airflow/api_request")

def safe_main_callable():
    from insert_records import main  # type: ignore
    return main()


def fetch_data():
    print("Fetching weather data from the API...")

default_args = {
    "owner": "airflow",
    "description": "A DAG to orchestrate the weather data pipeline",
    "catchup": False,
    "start_date": datetime.datetime(2026,2,15),
}
dag = DAG(
      dag_id="orchestrator",
    default_args=default_args,
    schedule=datetime.timedelta(minutes=1)
    )  
with dag:
      task1 = PythonOperator(
          task_id="fetch_weather_data",
          python_callable=safe_main_callable
      )