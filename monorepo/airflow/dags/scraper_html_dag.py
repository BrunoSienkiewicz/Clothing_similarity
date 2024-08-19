from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from kafka import KafkaProducer
from scripts.scrapper_html import scrape_html
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

dag = DAG(
    'scrapper_html_part_dag',
    default_args=default_args,
    description='amogus',
    schedule_interval='*/15 * * * *',  
    catchup=False,
    max_active_runs=1
)

def send_json_one_by_one():
    json_array = scrape_html()
    for json_var in json_array:
        send_message(json_var)

def send_message(json_obj):
    producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send('test_topic', json_obj)
    producer.flush()
    producer.close()

send_message_task = PythonOperator(
    task_id='send_json_one_by_one',
    python_callable=send_json_one_by_one,
    dag=dag,
)

send_message_task
