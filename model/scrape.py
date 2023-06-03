import os
import requests
import time
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from keras.preprocessing.image import image_utils


chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")


GRAILED_BASE_URL = "https://www.grailed.com/categories/"
GRAILED_CATEGORIES = [
    "sweatshirts-hoodies",
    "short-sleeve-t-shirts",
    "long-sleeve-t-shirts",
    "polos",
    "shirts-button-ups",
    "bottoms",
    "outerwear",
    "womenswear/dresses",
    "hats",
    "shorts",
    "womenswear/maxi-skirts",
    "womenswear/mini-skirts",
    "womenswear/bodysuits",
    "womenswear/blouses",
    "womenswear/hoodies"
]

CATEGORIES_TO_LABELS = {
    "sweatshirts-hoodies": "hoodie",
    "short-sleeve-t-shirts": "t-shirt",
    "long-sleeve-t-shirts": "longsleeve",
    "polos": "polo",
    "shirts-button-ups": "shirt",
    "bottoms": "pants",
    "outerwear": "outwear",
    "womenswear/dresses": "dress",
    "hats": "hat",
    "shorts": "shorts",
    "womenswear/maxi-skirts": "skirt",
    "womenswear/mini-skirts": "skirt",
    "womenswear/bodysuits": "body",
    "womenswear/blouses": "blouse",
    "womenswear/hoodies": "hoodie"
}


def get_requests(url, driver, scroll_pause_time=4, scroll_times=10):
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    request_list = []
    for request in driver.requests:
        if request.response:
            request_list.append(request)

    return request_list


def create_dataset(imgs : dict):
    columns = ["Image", "Label", "link", "date_added"]
    df = pd.DataFrame(columns=columns)
    for img in imgs.items():
        df = df.append({"Image": img[0], "Label": img[1][1], "link": img[1][2], "date_added": dt.datetime.isoformat(dt.datetime.now())}, ignore_index=True)
    return df


def insert_into_database(df : pd.DataFrame, database):
    for index, row in df.iterrows():
        database.insert({"Image": row["Image"], "Label": row["Label"], "link": row["link"], "date_added": row["date_added"]})


def scrape_images(categories=GRAILED_CATEGORIES):
    driver = webdriver.Chrome(options=chrome_options)
    for category in categories:
        url = GRAILED_BASE_URL + category
        request_list = get_requests(url, driver, scroll_times=1)
        imgs = {}
        for request in request_list:
            if request.url.startswith("https://process.fs.grailed.com"):
                imgs[request.path[-20:]] = [request.response.body]
                imgs[request.path[-20:]].append(CATEGORIES_TO_LABELS[category])
                imgs[request.path[-20:]].append("https://www.grailed.com" + request.path[:-20])
        for img in imgs.items():
            category_dir = "images/" + CATEGORIES_TO_LABELS[category] + "/"
            os.makedirs(category_dir, exist_ok=True)
            
            filename = img[0] + ".jpg"
            filepath = os.path.join(category_dir, filename)
            with open(filepath, "wb+") as f:
                try:
                    f.write(img[1][0])
                except:
                    pass
        soup = BeautifulSoup(driver.page_source, "lxml")
        soup_imgs = soup.findAll("div", {"class": "feed-item"})
        pass
    driver.quit()
    return imgs


def main():
    imgs = scrape_images()
    df = create_dataset(imgs)
    pass


if __name__ == "__main__":
    main()
        