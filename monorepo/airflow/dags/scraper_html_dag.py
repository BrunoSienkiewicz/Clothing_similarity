from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from kafka import KafkaProducer
from scripts.scrapper_html import scrape_html

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

def send_json_one_by_one():
    json_array = scrape_html()
    for json in json_array:
        send_message(json)

def send_message(json):
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    producer.send('test_topic', json)
    producer.flush()
    producer.close()

send_message_task = PythonOperator(
    task_id='send_json_one_by_one',
    python_callable=send_json_one_by_one,
    dag=dag,
)

send_json_one_by_one