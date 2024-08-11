import zipfile
import pandas as pd
from PIL import Image
from io import BytesIO
from datasets import load_dataset


def load_image_from_zip(zip_path, image_folder, image_id):
    with zipfile.ZipFile(zip_path) as z:
        with z.open(f'{image_folder}/{image_id}.jpg') as image_file:
            image = Image.open(BytesIO(image_file.read()))
            return image.convert("RGB")

class ZipDataset:
    def __init__(self, zip_path: str, image_folder: str, labels: list, **kwargs):
        self.zip_path = zip_path
        self.image_folder = image_folder
        self.labels = labels

        with zipfile.ZipFile(zip_path) as z:
            with z.open('images.csv') as metadata_file:
                self.metadata = pd.read_csv(metadata_file)
                self.metadata.set_index('image', inplace=True)
                self.metadata['label'].isin(labels)

        return load_dataset('pandas', data_files=self.metadata, **kwargs)





