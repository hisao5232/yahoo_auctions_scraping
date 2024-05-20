from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url='https://auctions.yahoo.co.jp/'
time.sleep(2)

def delete_ad():
    driver.find_element(By.CSS_SELECTOR,"div > a.Close-sc-uncojt.UslsY").click()

def condition():
    condition_new = driver.find_element(By.XPATH,"(//label[contains(@class,'CheckBox')]/descendant::span[contains(text(),'未使用')])[1]")
    condition_new.click()

def page_nation():
    while True:
        #次へクリック
        try:
            driver.find_element(By.CSS_SELECTOR,"li.Pager__list--next > a.Pager__link").click()
            print("page")
            time.sleep(3)
        except:
            break

def get_href():
    href_list=[]
    hrefs_elem=driver.find_elements(By.CSS_SELECTOR,"li.Product > div > a")
    for elem in hrefs_elem:
        href=elem.get_attribute("href")
        href_list.append(href)
    return href_list

def get_detail():
    title=driver.find_element(By.CSS_SELECTOR,"h1.ProductTitle__text").text
    price=driver.find_element(By.CSS_SELECTOR,"dd.Price__value").text
    try:
        send_fee=driver.find_element(By.CSS_SELECTOR,"span.Price__postageValue").text
    except:
        send_fee="0"

    print(title)
    print(price)
    print(send_fee)


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
    time.sleep(3)
    condition()
    time.sleep(1)
    hrefs = get_href()
    for href in hrefs:
        driver.get(href)
        time.sleep(1)
        get_detail()

    page_nation()

def get_photos(url=None):
    driver.get("https://page.auctions.yahoo.co.jp/jp/auction/o1136379660")
    photo_elems=driver.find_elements(By.CSS_SELECTOR,"a.ProductImage__link.cl-noclick-log")
    print(len(photo_elems))

if __name__ == "__main__":
    get_photos()
