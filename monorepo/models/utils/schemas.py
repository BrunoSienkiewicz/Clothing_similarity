MODEL_SCHEMA = {
    "type": "object",
    "properties": {
        "MODEL": {
            "type": "object",
            "properties": {
                "NAME": {"type": "string"},
                "VERSION": {"type": "string"},
                "TRAINING_PARAMETERS": {
                    "type": "object",
                    "properties": {
                        "num_train_epochs": {"type": "integer"},
                        "logging_dir": {"type": "string"},
                    },
                    "required": ["num_train_epochs"],
                    "additionalProperties": True,
                },
                "MODEL_PARAMETERS": {
                    "type": "object",
                },
            },
            "required": ["NAME", "VERSION", "TRAINING_PARAMETERS", "MODEL_PARAMETERS"],
        },
        "DATASET": {
            "type": "object",
            "properties": {
                "TYPE": {"type": "string"},
                "TRAIN_SPLIT": {"type": "number"},
                "ARGS": {"type": "object"},
            },
            "required": ["TYPE", "TRAIN_SPLIT", "ARGS"],
            "additionalProperties": False,
        },
    },
    "required": ["MODEL", "DATASET"],
}
