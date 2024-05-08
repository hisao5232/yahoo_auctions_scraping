from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url='https://auctions.yahoo.co.jp/'

def delete_ad():
    driver.find_element(By.CSS_SELECTOR,"div > a.Close-sc-uncojt.UslsY").click()

def search(keyword):
    driver.get(url)
    try:
        delete_ad()
    except:
        pass
    elm=driver.find_element(By.CSS_SELECTOR,"div > div > input")
    elm.send_keys(keyword)
    #検索ボタンクリック
    driver.find_element(By.CSS_SELECTOR,"input#acHdSchBtn").click()
    time.sleep(60)

def page_nation():
    while True:
        #次へクリック
        driver.find_element(By.CSS_SELECTOR,"li.Pager__list.Pager__list--next > a").click()

if __name__ == "__main__":
    search(keyword="Python")
