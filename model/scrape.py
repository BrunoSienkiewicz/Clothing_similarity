import os
import requests
import time
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup
from seleniumwire import webdriver as wiredriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from database import Database, ImageDatabase


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
        try:
            series = pd.Series([img[0], img[1][1], img[1][2], dt.datetime.isoformat(dt.datetime.now())], index=columns)
        except IndexError:
            continue
        df = pd.concat([df, series.to_frame().T], ignore_index=True)
    return df


def insert_dataset(imgs, images_info, images_binaries):
    df = create_dataset(imgs)
    for index, row in df.iterrows():
        images_info.insert(row.to_dict())
        if (imgs[row["Image"]][0][0] != 82):
            continue
        images_binaries.insert_binary(imgs[row["Image"]][0], f"{row['Image']}.jpg")


def scrape_images(categories=GRAILED_CATEGORIES):
    wdriver = wiredriver.Chrome(options=chrome_options)
    for category in categories:
        url = GRAILED_BASE_URL + category
        request_list = get_requests(url, wdriver, scroll_times=2)
        imgs = {}
        for request in request_list:
            if request.url.startswith("https://process.fs.grailed.com"):
                imgs[request.path[-20:]] = [request.response.body]
                imgs[request.path[-20:]].append(CATEGORIES_TO_LABELS[category])

        # driver = webdriver.Chrome(options=chrome_options)
        # driver.get(url)
        WebDriverWait(wdriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
        page_content = wdriver.page_source
        soup = BeautifulSoup(page_content, "lxml")
        images = soup.find_all("img")

        img_to_link = {}
        for image in images:
            img_to_link[image["src"][-20:]] = image['alt']

        for img_to_link_key in img_to_link.keys():
            if img_to_link_key in imgs.keys():
                imgs[img_to_link_key].append(img_to_link[img_to_link_key])

    wdriver.quit()
    return imgs


def main():
    imgs = scrape_images(["sweatshirts-hoodies"])
    df = create_dataset(imgs)
    pass


if __name__ == "__main__":
    main()
        