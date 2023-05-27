import os
import requests
import time
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


def main():
    driver = webdriver.Chrome(options=chrome_options)
    for category in GRAILED_CATEGORIES:
        url = GRAILED_BASE_URL + category
        request_list = get_requests(url, driver, scroll_times=3)
        imgs = []
        for request in request_list:
            if request.url.startswith("https://process.fs.grailed.com"):
                imgs.append(request.response.body)
        for img in imgs:
            category_dir = "images/" + CATEGORIES_TO_LABELS[category] + "/"
            os.makedirs(category_dir, exist_ok=True)
            
            filename = str(time.time()) + ".jpg"
            filepath = os.path.join(category_dir, filename)
            with open(filepath, "wb+") as f:
                f.write(img)
    driver.quit()


if __name__ == "__main__":
    main()
        