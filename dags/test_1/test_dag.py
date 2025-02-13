from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
 
# Создадим объект класса DAG
dag =  DAG('dag_yarik', schedule_interval=timedelta(days=1), start_date=days_ago(1))

# Создадим несколько шагов, которые будут параллельно исполнять dummy(пустые)команды
t1 = DummyOperator(task_id='task_1', dag=dag)
t2 = DummyOperator(task_id='task_2', dag=dag)
t3 = DummyOperator(task_id='task_3', dag=dag)
t4 = DummyOperator(task_id='task_4', dag=dag)

# Настройка зависимостей
t1 >> [t2, t3] >> t4