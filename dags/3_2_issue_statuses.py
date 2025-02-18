from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator


# Функция, которая будет вызываться в PythonOperator
def task_that_fails1():
    return 1 / 0


def task_that_fails2():
    return 1 / 0


def task_that_success():
    return True


# Создаём DAG
dag = DAG(
    'dag1',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,  # Запускать DAG вручную
)

# Задача, которая вызывает ошибку
task1 = PythonOperator(
    task_id='task_that_fails1',
    python_callable=task_that_fails1,
    dag=dag,
)

# Задача, которая вызывает ошибку
task2 = PythonOperator(
    task_id='task_that_fails2',
    python_callable=task_that_fails2,
    dag=dag,
)

# Задача, которая вызывает ошибку
task3 = PythonOperator(
    task_id='task_that_success',
    python_callable=task_that_success,
    # Данная задача будет ожидать определенное поведение
    # В данном примере она ждет что все дочерние задачи завершатся ошибкой
    trigger_rule='all_failed',
    dag=dag,
)

[task1, task2] >> task3
