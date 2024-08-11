from datasets import Dataset
from vit.model import ViT


class SaveOutput:
    def __init__(self):
        self.outputs = []
        
    def __call__(self, module, module_in, module_out):
        self.outputs.append(module_in)
        
    def clear(self):
        self.outputs = []


def test(model : ViT, test_ds : Dataset):
    save_output = SaveOutput()
    hook_handles = []
    for layer in model.modules():
        if str(layer) == 'Linear(in_features=768, out_features=10, bias=True)':
            handle = layer.register_forward_hook(save_output)
            hook_handles.append(handle)
    
    outputs = model.trainer.predict(test_ds)
    
    return outputs.metrics
