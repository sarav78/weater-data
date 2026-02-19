import datetime
import sys
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import odcker.types import mount
def fetch_data():
    print("Fetching weather data from the API...")

default_args = {
    "owner": "airflow",
    "description": "A DAG to orchestrate the weather data pipeline",
    "catchup": False,
    "start_date": datetime.datetime(2026,2,15),
}
dag = DAG(
      dag_id="dbt_orchestrator",
    default_args=default_args,
    schedule=datetime.timedelta(minutes=1)
    )  
with dag:
      task2 = DockerOperator(
        task_id = 'transform_data_task'
        image = 'ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command = 'run',
        working_dir = '/usr/app/',
        Mounts = [
            Mount(source='repos/weater-data/dbt/my_project/my_project',
                  target='/usr/app/',
                  type='bind'),
             Mount(source='/repos/weater-data/dbt/profiles.yml',
                  target='/root/.dbt/profiles.yml',
                  type='bind'),
            ],
        network_mode ='my-network',
        docker_url = 'unix://var/run/docker.sock',
        auto_remove='success'
      )