FROM postgres:13

# Install build dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    postgresql-server-dev-13

# Clone the pgvector repository
RUN git clone https://github.com/pgvector/pgvector.git

# Build and install pgvector
RUN cd pgvector && make && make install

# Clean up
RUN apt-get remove -y \
    git \
    build-essential \
    postgresql-server-dev-13 && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* pgvector

