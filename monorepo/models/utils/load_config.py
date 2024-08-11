import yaml
import jsonschema   
from utils.schemas import MODEL_SCHEMA


def load_config(config_path):
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f)
    
    jsonschema.validate(cfg, MODEL_SCHEMA)
    
    return cfg
