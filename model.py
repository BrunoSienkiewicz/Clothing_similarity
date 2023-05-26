from transformers import ViTModel
from transformers.modeling_outputs import SequenceClassifierOutput
from transformers import TrainingArguments, Trainer
from transformers import default_data_collator
import torch.nn as nn
from datasets import load_metric
from datasets import Dataset
import numpy as np
import torch
import json


class ViTForImageClassification(nn.Module):
    def __init__(self, num_labels=10, vector_length=1000):
        super(ViTForImageClassification, self).__init__()
        self.vit = ViTModel.from_pretrained('google/vit-base-patch16-224-in21k')
        self.dropout = nn.Dropout(0.1)
        self.last_layer = nn.Linear(self.vit.config.hidden_size, num_labels)
        self.num_labels = num_labels

        self.args = TrainingArguments(
            f"test-clothing",
            evaluation_strategy = "epoch",
            save_strategy = "epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=10,
            per_device_eval_batch_size=4,
            num_train_epochs=3,
            weight_decay=0.01,
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            logging_dir='logs',
        )

        self.data_collator = default_data_collator

    def forward(self, pixel_values, labels):
        outputs = self.vit(pixel_values=pixel_values)
        output = self.dropout(outputs.last_hidden_state[:,0])
        logits = self.last_layer(output)

        loss = None
        if labels is not None:
          loss_fct = nn.CrossEntropyLoss()
          loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))

        return SequenceClassifierOutput(
            loss=loss,
            logits=logits,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )
    
    def compute_metrics(eval_pred):
        metric = load_metric("accuracy")

        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return metric.compute(predictions=predictions, references=labels)
    
    def train(self, train_ds, val_ds):
        self.trainer = Trainer(
            model=self,
            args=self.args,
            train_dataset=train_ds,
            eval_dataset=val_ds,
            data_collator=self.data_collator,
            compute_metrics=self.compute_metrics,
        )
        self.trainer.train()

    def save_model(self, path):
        torch.save(self.state_dict(), path)


class SaveOutput:
    def __init__(self):
        self.outputs = []
        
    def __call__(self, module, module_in, module_out):
        self.outputs.append(module_in)
        
    def clear(self):
        self.outputs = []


def evaluate_model(model : ViTForImageClassification, test_ds : Dataset):
    save_output = SaveOutput()
    hook_handles = []
    for layer in model.modules():
        if str(layer) == 'Linear(in_features=768, out_features=10, bias=True)':
            handle = layer.register_forward_hook(save_output)
            hook_handles.append(handle)
    
    outputs = model.trainer.predict(test_ds)
    
    return outputs.metrics
