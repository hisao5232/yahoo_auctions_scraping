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
    time.sleep(2)
    photo_elems=driver.find_elements(By.CSS_SELECTOR,"li.ProductImage__thumbnail")

    for photo_elem in photo_elems:
        photo_elem.click()
        time.sleep(1)
        img=driver.find_element(By.CSS_SELECTOR,'li.is-on > div > img').get_attribute("src")
        print(img)

def get_seller():
    driver.get("https://page.auctions.yahoo.co.jp/jp/auction/o1136379660")
    time.sleep(2)
    href_seller=driver.find_element(By.CSS_SELECTOR,"a.Seller__selling").get_attribute("href")
    driver.get(href_seller)
    time.sleep(2)
    seller_elems=driver.find_elements(By.CSS_SELECTOR,"a.Product__titleLink")
    print(len(seller_elems))
    for seller_elem in seller_elems:
        seller_href=seller_elem.get_attribute("href")
        print(seller_href)
        driver.get(seller_href)
        time.sleep(2)
        print("取得")

if __name__ == "__main__":
    get_seller()
