# Библиотеки для работы с Airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from main import extract_date, transform_data, upload_data, check_and_delete_data, URL, CH_CLIENT

with DAG(
        'Examples_ETL',
        schedule_interval=None,  # Запуск каждый день
        start_date=datetime(2024, 1, 1),
        tags=['examples']
) as dag:
    task_extract_date = PythonOperator(
        task_id='extract_date',
        python_callable=extract_date,
        op_args=[URL, 'currency.json'],
    )

    task_transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_args=['currency.json', 'currency.csv', '01/06/2024'],
    )

    task_check_and_delete_data = PythonOperator(
        task_id='check_and_delete_data',
        python_callable=check_and_delete_data,
        op_args=['exchange_rate', CH_CLIENT, '01/06/2024'],
    )

    task_upload_data = PythonOperator(
        task_id='upload_data',
        python_callable=upload_data,
        op_kwargs={'csv_file': 'currency.csv',
                   'table_name': 'exchange_rate',
                   'client': CH_CLIENT},
    )

    task_extract_date >> task_transform_data >> task_check_and_delete_data >> task_upload_data
