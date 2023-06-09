from preprocess_data import load_data, load_images, split_data, preprocess_images, filter_data, label_data
from model import ViTForImageClassification, evaluate_model
from database import Database, ImageDatabase, retrieve_and_display_image
from scrape import scrape_images, create_dataset
from random import choice


def main():
    # imgs = scrape_images(["bottoms", "short-sleeve-t-shirts", "sweatshirts-hoodies"])
    # df = create_dataset(imgs)
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



if __name__ == "__main__":
    main()