from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from kafka import KafkaProducer

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

dag = DAG(
    'kafka_producer_dag',
    default_args=default_args,
    description='A simple Kafka producer DAG',
    schedule_interval='*/5 * * * * *',  
    catchup=False,
    max_active_runs=1
)

def send_message():
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    producer.send('test_topic', b'Test message from Airflow')
    producer.flush()
    producer.close()

send_message_task = PythonOperator(
    task_id='send_message',
    python_callable=send_message,
    dag=dag,
)

send_message_task

