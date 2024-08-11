import argparse
import numpy as np
from vit.model import ViT
from utils.load_config import load_config
from custom_datasets.zip_dataset import ZipDataset
from custom_datasets.sql_dataset import SQLImageDataset
from transformers import TrainingArguments, Trainer
from transformers import default_data_collator
from datasets import Dataset
from datasets import load_metric


def compute_metrics(eval_pred):
    metric = load_metric("accuracy")

    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return metric.compute(predictions=predictions, references=labels)


def train(model: ViT, train_ds: Dataset, val_ds: Dataset, cfg: dict={}):
        data_collator = default_data_collator

        args = TrainingArguments(
            "test-clothing",
            evaluation_strategy = "epoch",
            save_strategy = "epoch",
            learning_rate=cfg.get("learning_rate", 2e-5),
            per_device_train_batch_size=10,
            per_device_eval_batch_size=4,
            num_train_epochs=cfg.get("num_train_epochs", 3),
            weight_decay=cfg.get("weight_decay", 0.01),
            load_best_model_at_end=True,
            metric_for_best_model=cfg.get("metric_for_best_model", "accuracy"),
            logging_dir=cfg.get("logging_dir", "./logs"),
        )

        trainer = Trainer(
            model=model,
            args=args,
            train_dataset=train_ds,
            eval_dataset=val_ds,
            data_collator=data_collator,
            compute_metrics=compute_metrics,
        )
        trainer.train()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg_file", type=str, required=True)

    args = parser.parse_args()
    cfg = load_config(args.cfg_file)

    custom_datasets = [
        ZipDataset,
        SQLImageDataset,
    ]

    train_ds = None
    val_ds = None
    for custom_dataset in custom_datasets:
        if cfg["DATASET"]["TYPE"] == custom_dataset.__name__:
            train_ds = custom_dataset(**cfg["DATASET"]["ARGS"])
            train_ds, val_ds = train_ds.train_test_split(test_size=cfg["DATASET"]["TRAIN_SPLIT"])
            break
    if not train_ds:
        raise ValueError(f"Dataset type {cfg['DATASET']['TYPE']} not supported.")

    model = ViT(**cfg["MODEL"]["MODEL_PARAMETERS"])
    train(model, train_ds, val_ds, cfg["MODEL"]["TRAINING_PARAMETERS"])
