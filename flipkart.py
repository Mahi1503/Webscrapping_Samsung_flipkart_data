from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import random
import os
import numpy as np
import pandas as pd

s = Service("chromedriver.exe")
driver = webdriver.Chrome(service=s)

os.chdir(r"D:\Jupyter\flipkart")
for i in range(1,37):
    driver.get("https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&p%5B%5D=facets.brand%255B%255D%3DSAMSUNG&page={}".format(i))
    html = driver.page_source
    time.sleep(random.uniform(5, 15))
    with open(f"flipkart_data{i}.html","w",encoding="utf-8") as f:
        f.write(html)
file_list = os.listdir()
cwd = os.getcwd()
os.chdir(cwd)

merged_soup = BeautifulSoup("<html><head></head><body></body></html>", "html.parser")

for file in file_list:
    with open(file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        if soup.body:
            merged_soup.body.extend(soup.body.contents)

output_file = "merged.html"
with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.write(str(merged_soup.prettify()))

with open("merged.html",encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html,"lxml")
container = soup.find_all("div",class_="tUxRFH")

model_name = []
photo_img_url = []
star_rating = []
rating = []
review = []
discount_price = []
original_price = []
ram = []
display = []
camera = []
battery = []
processor = []
warranty = []
prod = 1

for i in container:
    model_name.append(i.find("div", class_="KzDlHZ").text.strip())
    photo_img_url.append(i.find("img", class_="DByuf4")["src"])
    try:
        star_rating.append(i.find("div", class_="XQDdHH").text.strip())
    except:
        star_rating.append("0")

    data = i.find_all("span", class_="Wphh3N")
    if data == []:
        rating.append(np.nan)
        review.append(np.nan)

    else:
        for j in data:
            try:
                text = j.text.strip()  # Get text safely
                words = text.split()  # Split into words
                if len(words) >= 1:
                    rating.append(words[0])
                else:
                    rating.append(np.nan)

                if len(words) >= 4:
                    review.append(words[3])
                else:
                    review.append(np.nan)
            except Exception as e:
                print(f"Error: {e}")
                rating.append(np.nan)
                review.append(np.nan)

    try:
        discount_price.append(i.find("div", class_="Nx9bqj _4b5DiR").text.strip())
    except:
        discount_price.append(np.nan)
    try:
        original_price.append(i.find("div", class_="yRaY8j ZYYwLA").text.strip())
    except:
        original_price.append(np.nan)

    li = i.find_all("li", class_="J+igdf")
    spec = []
    for i in li:
        spec.append(i.text.strip())
    ram.append(spec[0])
    display.append(spec[1])
    camera.append(spec[2])
    battery.append(spec[3])
    try:
        processor.append(spec[4])
    except:
        processor.append(np.nan)
    try:
        warranty.append(spec[5])
    except:
        warranty.append(np.nan)

samsung_df = pd.DataFrame({
    "name" : model_name,
    "photo_img_url" : photo_img_url,
    "star_rating" : star_rating,
    "rating" : rating,
    "review" : review,
    "discount_price" : discount_price,
    "original_price" : original_price,
    "ram" : ram,
    "display" : display,
    "camera" : camera,
    "battery" : battery,
    "processor":processor,
    "warranty" : warranty
})

samsung_df.to_csv("samsung.csv",encoding="utf-8")