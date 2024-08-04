
CREATE KEYSPACE IF NOT EXISTS items WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE items;
CREATE TABLE items (id bigint, title text, category text, image_link text, listing_link text, ingested_at timestamp, PRIMARY KEY (id)); 
CREATE INDEX items_category ON items (category);
CREATE TABLE item_features (item_id bigint, feature text, value text, PRIMARY KEY (item_id, feature));
CREATE INDEX item_features_item_id_feature ON item_features (item_id, feature);

CREATE KEYSPACE IF NOT EXISTS embeddings WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE embeddings;
CREATE TABLE embeddings (model_id bigint, item_id bigint, embedding vector, PRIMARY KEY (model_id, item_id));

CREATE KEYSPACE IF NOT EXISTS models WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE models;
CREATE TABLE models (id bigint, name text, version bigint, PRIMARY KEY (id));

