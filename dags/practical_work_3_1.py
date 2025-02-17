from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator

dag = DAG(
    'practical_work_3_1',
    schedule_interval='@daily',
)

task_1 = DummyOperator('task_1', dag=dag)
task_2 = DummyOperator('task_2', dag=dag)
