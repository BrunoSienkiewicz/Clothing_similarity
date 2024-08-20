import json

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from kafka import KafkaConsumer

from scripts.listing_scraper import scrape_html, save_info

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

dag = DAG(
    'kafka_consumer_dag',
    default_args=default_args,
    description='A simple Kafka consumer DAG',
    schedule_interval='*/10 * * * * *',
    catchup=False,
    max_active_runs=1
)

def consume_message():
    consumer = KafkaConsumer('test_topic', bootstrap_servers='kafka:9092')
    for message in consumer:
        print(f"Received message: {message.value.decode('utf-8')}")
        listing = json.loads(message.value.decode('utf-8'))
        parsed_listing = scrape_html(listing["listing_link"])
        save_info(parsed_listing, listing["img_link"])
        break  # Consume one message and exit
    consumer.close()

consume_message_task = PythonOperator(
    task_id='consume_message',
    python_callable=consume_message,
    dag=dag,
)

consume_message_task

