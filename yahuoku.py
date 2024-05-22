from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url='https://auctions.yahoo.co.jp/'
detail_list=[]
title_list=[]
price_list=[]
send_fee_list=[]
img_list=[]
photo_list=[]
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
    d_detail={}
    title=driver.find_element(By.CSS_SELECTOR,"h1.ProductTitle__text").text
    price=driver.find_element(By.CSS_SELECTOR,"dd.Price__value").text
    try:
        send_fee=driver.find_element(By.CSS_SELECTOR,"span.Price__postageValue").text
    except:
        send_fee="0"

    d_detail={'title':title,'price':price,'send_fee':send_fee}
    detail_list.append(d_detail)

def search(keyword):
    driver.get(url)
    try:
        #広告を消す
        delete_ad()
    except:
        pass
    #キーワード入力
    elm=driver.find_element(By.CSS_SELECTOR,"div > div > input")
    elm.send_keys(keyword)

    #検索ボタンクリック
    driver.find_element(By.CSS_SELECTOR,"input#acHdSchBtn").click()
    time.sleep(3)

    #絞り込み
    condition()
    time.sleep(1)
    auction=driver.find_element(By.CSS_SELECTOR,"a.Tab__itemInner").get_attribute("href")

    #オークションのみ
    driver.get(auction)
    time.sleep(2)

    #商品の詳細取得
    hrefs = get_href()
    for href in hrefs:
        driver.get(href)
        time.sleep(1)
        get_detail()
        get_photos()

    #page_nation()

    df_detail=pd.DataFrame(detail_list)
    df_photo = pd.DataFrame(photo_list)
    df_concat= pd.concat([df_detail, df_photo], axis=1)
    df_concat.to_excel("yahuoku_deta.xlsx")

def get_photos(url=None):
    d_img={}
    #写真要素取得
    photo_elems=driver.find_elements(By.CSS_SELECTOR,"li.ProductImage__thumbnail")
    img=driver.find_element(By.CSS_SELECTOR,'li.is-on > div > img').get_attribute("src")
    d_img["picture_1"]=img
    i=1

    #写真クリック、画像取得
    for photo_elem in photo_elems:
        photo_elem.click()
        time.sleep(1)
        img=driver.find_element(By.CSS_SELECTOR,'li.is-on > div > img').get_attribute("src")
        d_img[f'picture_{i}']=img
        i=i+1
    
    photo_list.append(d_img)
        

def get_seller():
    driver.get("https://page.auctions.yahoo.co.jp/jp/auction/h1137145963")
    time.sleep(2)
    href_seller=driver.find_element(By.CSS_SELECTOR,"a.Seller__selling").get_attribute("href")
    driver.get(href_seller)
    time.sleep(2)
    seller_elems=driver.find_elements(By.CSS_SELECTOR,"a.Product__titleLink")
    print(len(seller_elems))
    
    seller_href_list=[]
    for seller_elem in seller_elems:
        seller_href=seller_elem.get_attribute("href")
        seller_href_list.append(seller_href)

    for seller_href in seller_href_list:
        driver.get(seller_href)
        time.sleep(2)
        get_detail()

if __name__ == "__main__":
    search("基本情報技術者試験")
