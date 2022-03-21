import airflow

from airflow import DAG

from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}

dag = DAG(
    dag_id='dag01',
    default_args=args,
    schedule_interval='@daily',
    dagrun_timeout=timedelta(minutes=60)
)

t1 = BashOperator(
    task_id='task01',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='task02_sleep',
    bash_command='sleep 10',
    retries=3,
    dag=dag
)


t3 = BashOperator(
    task_id='task03_saida',
    bash_command='date > /opt/airflow/outputs/date_output.txt',
    retries=3,
    dag=dag
)



t1 >> t2 >> t3