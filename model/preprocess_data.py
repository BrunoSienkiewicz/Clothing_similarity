import zipfile
import io
import os
import pandas as pd
import numpy as np
from keras.preprocessing.image import image_utils
from datasets import Dataset
from datasets import Features, ClassLabel, Array3D
from transformers import ViTImageProcessor
import random


def load_data():
    if not os.path.exists('./clothing-dataset/images.csv'):
        zf = zipfile.ZipFile(io.BytesIO('clothing-dataset.zip'), "r")
        zf.extractall()

    df = pd.read_csv('./clothing-dataset/images.csv').set_index('image')
    return df


def label_data(df : pd.DataFrame):
    top_labels = pd.DataFrame(df.groupby('label').size().reset_index().sort_values(0,ascending = False)['label'])
    top_labels = top_labels[top_labels.label!='Not sure']
    top_labels = top_labels[top_labels.label!='Other']
    top_labels = top_labels[top_labels.label!='Top']
    top_labels = top_labels[top_labels.label!='Skip']
    top_labels = top_labels[top_labels.label!='Undershirt']

    top_labels_list = sorted(list(top_labels['label']))
    top_labels['label_num'] = top_labels['label'].apply(lambda x: top_labels_list.index(x))

    return top_labels, top_labels_list


def filter_data(df : pd.DataFrame, top_labels : pd.DataFrame):
    data_filtered = pd.merge(df.reset_index(), top_labels).set_index('image')
    data_filtered['label_str'] = data_filtered['label']
    data_filtered['label'] = data_filtered['label_num']

    return data_filtered


def load_images(data_filtered : pd.DataFrame):
    labeled_data = []
    for i, item in enumerate(os.listdir( './clothing-dataset/images' )):
        path = os.path.join('./clothing-dataset/images', item) 
        img = image_utils.load_img(path, target_size=(32, 32))
        
        x = image_utils.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])[0].tolist()

        try:
            label = data_filtered.loc[item[:-4],'label']
            labeled_data.append({'img':images, 'label':label, 'index':item[:-4]})
        except:
            label = 'no_data'

    return labeled_data


def split_data(data_filtered : pd.DataFrame, labeled_data : list):
    ind = data_filtered.index.tolist()
    random.shuffle(ind)

    n = len(data_filtered)
    p_train = 0.6
    p_val = 0.2
    n_train = int(p_train*n)
    n_val = int(p_val*n)
    train_ind = ind[:n_train]
    val_ind = ind[n_train:(n_train+n_val)]
    test_ind = ind[(n_train+n_val):]

    train_img = []
    val_img = []
    test_img = []
    train_label = []
    val_label = []
    test_label = []
    test_ids = []

    for img in labeled_data:
        if img['index'] in train_ind:
            train_img.append(img['img'])
            train_label.append(img['label'])
        elif img['index'] in val_ind:
            val_img.append(img['img'])
            val_label.append(img['label'])
        elif img['index'] in test_ind:
            test_img.append(img['img'])
            test_label.append(img['label'])
            test_ids.append(img['index'])

    return train_img, val_img, test_img, train_label, val_label, test_label, test_ids


def preprocess_images(top_labels_list : list, train_img : list, val_img : list, test_img : list, train_label : list, val_label : list, test_label : list):
    train_ds = preprocess_images_list(top_labels_list, train_img, train_label)
    val_ds = preprocess_images_list(top_labels_list, val_img, val_label)
    test_ds = preprocess_images_list(top_labels_list, test_img, test_label)
    
    return train_ds, val_ds, test_ds


def preprocess_images_list(top_labels_list : list, list_img : list, list_label : list):
    ds = Dataset.from_dict({'img':list_img,'label':list_label})

    feature_extractor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224-in21k')

    def preprocess(ds):
        images = ds['img']

        images = [np.array(image, dtype=np.uint8) for image in images]
        images = [np.moveaxis(image, source=-1, destination=0) for image in images]

        inputs = feature_extractor(images=images)
        ds['pixel_values'] = inputs['pixel_values']

        return ds
    
    features = Features({
        'label': ClassLabel(names = top_labels_list),
        'img': Array3D(dtype="int64", shape=(3,32,32)),
        'pixel_values': Array3D(dtype="float32", shape=(3, 224, 224)),
    })
    
    ds = ds.map(preprocess, batched=True, features=features)
    
    return ds


def main():
    df = load_data()
    print(df.head())
    top_labels, top_labels_list = label_data(df)
    print(top_labels)
    data_filtered = filter_data(df, top_labels)
    print(data_filtered.head())
    labeled_data = load_images(data_filtered)
    print(labeled_data[0])
    train_img, val_img, test_img, train_label, val_label, test_label, test_ids = split_data(data_filtered, labeled_data)
    print(len(train_img), len(val_img), len(test_img))
    train_ds, val_ds, test_ds = preprocess_images(top_labels_list, train_img, val_img, test_img, train_label, val_label, test_label)
    print(train_ds)
    print(val_ds)
    print(test_ds)

if __name__ == "__main__":
    main()