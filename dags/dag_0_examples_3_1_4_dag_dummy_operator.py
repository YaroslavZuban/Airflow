from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator

dag = DAG('0_examples_3_1_4_dag_dummy_operator',
          schedule_interval=timedelta(days=1),
          start_date=days_ago(1),
          tags=['examples']
          )

t1 = DummyOperator(task_id='task_1', dag=dag)