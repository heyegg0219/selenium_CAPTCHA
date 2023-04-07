from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import io
import requests
from google.cloud import vision
from bs4 import BeautifulSoup
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_vision.json'
url = "https://www.etax.nat.gov.tw"
company_code = input(str("請輸入統編號碼:"))
options = Options()
options.add_argument("--disable-notifications")

chrome = webdriver.Chrome('./chromedriver', chrome_options=options)

chrome.get("https://www.etax.nat.gov.tw/etwmain/etw113w1/ban/query")
chrome.find_element(By.ID, "ban").send_keys(company_code)
# chrome.find_element(By.ID, "btnGo").send_keys(Keys.ENTER)
time.sleep(3)
soup = BeautifulSoup(chrome.page_source, 'html.parser')

data = soup.find_all('div', {'class': 'etw-captcha d-flex'})

# print(data)


for image in data:
    a_1 = image.find("img", class_="mr-2")
    img_link = url + a_1.get("src")  # 團片連結
    print(img_link)
    jpg = requests.get(img_link)
    f = open(f'static/{company_code}.jpg', 'wb')
    f.write(jpg.content)
    f.close()

    client = vision.ImageAnnotatorClient()
    path = os.path.abspath('static/44629107.jpg')
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    for index, text in enumerate(texts):
        if index < 1:
            print(text.description.replace(' ', ''))
        else:
            break
        chrome.find_element(By.XPATH, "//*[@id='captchaText']").send_keys(text.description.replace(' ', ''))
        chrome.find_element(By.XPATH, "//*[@id='queryForm']/div[2]/div[2]/button").click()

time.sleep(8)
