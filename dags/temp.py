from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime


def my_func(hello, date, **context):
    print(hello)
    print(date)
    print(context['ds'])


with DAG('my_dag', schedule_interval='@daily',
         start_date=datetime(2024, 1, 1),
         end_date=datetime(2024, 1, 4)) as dag:
    python_task = PythonOperator(
        task_id='python_task',
        python_callable=my_func,
        op_kwargs={
            'hello': 'Hello World',
            'date': '{{ ds }}'
        },
    )
