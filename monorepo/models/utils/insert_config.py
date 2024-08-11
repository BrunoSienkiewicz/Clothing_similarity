import jsonschema
from utils.schemas import MODEL_SCHEMA


def insert_config(cfg):
    jsonschema.validate(cfg, MODEL_SCHEMA)
