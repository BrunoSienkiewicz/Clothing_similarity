FROM postgres:13

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    postgresql-server-dev-13

RUN git clone https://github.com/pgvector/pgvector.git
RUN cd pgvector && make && make install

RUN apt-get remove -y \
    git \
    build-essential \
    postgresql-server-dev-13 && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* pgvector

COPY schema.sql /docker-entrypoint-initdb.d/schema.sql;
COPY init-airflow-db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init-airflow-db.sh

