import requests
import progressManager as pm
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd


def getRealtimePrice():

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome()

    url = 'http://finance.daum.net/domestic/all_stocks?market=KOSPI'

    dict = {}

    driver.get(url)
    # driver.implicitly_wait(100)
    sleep(5)
    tds = driver.find_elements_by_xpath(
        "//span[@data-realtime-trade-price='yes']")
    print(len(tds))
    pm.progress.setProgressGage(3)
    names = driver.find_elements_by_class_name("txt")
    print(len(names))
    pm.progress.setProgressGage(6)
    df = pd.DataFrame(columns=['stockName', 'price_now'])
    pm.progress.setProgressGage(24)
    for i in range(0, len(names)):
        df.loc[i] = [names[i].text, tds[i].text]
        pm.progress.setProgressGage(24+(75/len(names)*i))
    df.to_excel('stocks.xlsx', index=False)
    pm.progress.setProgressGage(100)
        # def getPrices:
        # response = requests.get('http://finance.daum.net/domestic/all_stocks?market=KOSPI')
        # soup = BeautifulSoup(response.text,'html.parser')

        # response = urlopen('http://finance.daum.net/domestic/all_stocks?market=KOSPI').read()

        # soup = BeautifulSoup(response, 'html.parser')

        # print(soup)
    driver.quit()
