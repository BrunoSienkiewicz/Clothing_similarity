FROM python:3.9

RUN pip install \
    mlflow \
    psycopg2 \
    boto3 && \
    mkdir /mlflow/

EXPOSE 5000

CMD mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --artifacts-destination $MLFLOW_ARTIFACT_ROOT \
    --backend-store-uri $MLFLOW_TRACKING_URI
