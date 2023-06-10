from preprocess_data import load_data, load_images, load_images_from_database, split_data, split_data_from_database, preprocess_images, filter_data, label_data, label_data_from_database
from model import ViTForImageClassification, evaluate_model
from database import Database, ImageDatabase, retrieve_and_display_image
from scrape import scrape_images, create_dataset
from random import choice
import tensorflow as tf

def scrape_and_display_images():
    imgs = scrape_images(["bottoms", "short-sleeve-t-shirts", "sweatshirts-hoodies"])
    df = create_dataset(imgs)
    images_info = Database("Images", "images_info")
    images_binaries = ImageDatabase("Images", "images_binaries")

    df = images_info.load_as_df()
    print(df.head())

    image_names = df["Image"].tolist()
    for i in range(5):
        image_name = choice(image_names)
        print(df.loc[df["Image"] == image_name].link)
        try:
            retrieve_and_display_image(images_binaries, image_name + ".jpg")
        except:
            print("Image not found")


def load_and_preprocess_images_from_database():
    images_info = Database("Images", "images_info")
    images_binaries = ImageDatabase("Images", "images_binaries")
    df = images_info.load_as_df()
    print(df.head())
    print(df.shape)
    top_labels, top_labels_list = label_data_from_database(df)
    labeled_data = load_images_from_database(images_info, images_binaries)
    print(labeled_data[0])
    train_img, val_img, test_img, train_label, val_label, test_label, test_ids = split_data_from_database(df, labeled_data)
    train_ds, val_ds, test_ds = preprocess_images(top_labels_list, train_img, val_img, test_img, train_label, val_label, test_label)

    return train_ds, val_ds, test_ds


def load_and_preprocess_images_from_file():
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

    return train_ds, val_ds, test_ds


def load_and_train_model(model, train_ds, val_ds, test_ds):
    path_to_model = "/model/"
    model = ViTForImageClassification()
    # model.load_model(path_to_model)
    train_ds, val_ds, test_ds = load_and_preprocess_images_from_file()
    # train_ds, val_ds, test_ds = load_and_preprocess_images_from_database()
    model.train(train_ds, val_ds)
    evaluate_model(model, test_ds)
    model.save_model(path_to_model)


def main():
    load_and_train_model()


if __name__ == "__main__":
    main()