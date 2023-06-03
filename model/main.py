from preprocess_data import load_data, load_images, split_data, preprocess_images, filter_data, label_data
from model import ViTForImageClassification, evaluate_model
from database import Database
from scrape import scrape_images, create_dataset, insert_into_database


def main():
    # imgs = scrape_images(["sweatshirts-hoodies"])
    # df = create_dataset(imgs)
    database = Database("Images", "Images_info")
    # insert_into_database(df, database)
    df = database.load_as_df()
    print(df.head())


if __name__ == "__main__":
    main()