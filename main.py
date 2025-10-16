from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common import keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Chromeオプション設定
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # GUIなし
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Yahoo!オークションURL
url = 'https://auctions.yahoo.co.jp/'

# データ格納リスト
detail_list = []
photo_list = []


# -----------------------------------------
# 共通ユーティリティ
# -----------------------------------------
def wait_for_page_ready(driver, timeout=10):
    """JavaScriptのロードが完了するまで待つ"""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    time.sleep(1.5)  # React描画待ち（Yahoo特有）

def scroll_to_bottom(driver, wait_time=2, max_waits=20):
    """
    ページの一番下まで自動スクロールして、全商品を読み込む。
    wait_time: 各スクロール後に待機する秒数
    max_waits: 同じ高さが続く最大回数（無限ループ防止）
    """
    print("🔽 ページの最下部までスクロール中...")

    last_height = driver.execute_script("return document.body.scrollHeight")
    same_height_count = 0

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_time)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            same_height_count += 1
            if same_height_count >= max_waits:
                print("✅ ページの最下部まで到達しました。")
                break
        else:
            same_height_count = 0  # 高さが変わったらカウンターリセット

        last_height = new_height

    # スクロール後に件数を確認
    try:
        count_elem = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.Option--count > button > span.Option__selected"))
        )
        count_text = count_elem.text.strip()
        print(f"📊 現在の表示件数: {count_text}")
    except Exception as e:
        print("⚠️ 件数の要素が見つかりませんでした。")
        print(f"  詳細: {e}")

# -----------------------------------------
# 検索・抽出系
# -----------------------------------------
def delete_ad():
    """広告を閉じる"""
    try:
        driver.find_element(By.CSS_SELECTOR, "div > a.Close-sc-uncojt.UslsY").click()
        print("🧹 広告を閉じました")
    except:
        pass

def condition():
    """未使用商品のみチェック"""
    try:
        # CSSセレクターで「未使用」チェックボックスをクリック
        condition_new = driver.find_element(
            By.CSS_SELECTOR,
            "#allContents > div.l-wrapper.cf > div.l-contents > div.l-contentsMain > div.l-contentsSide > div.Filters > div:nth-child(5) > div > ul:nth-child(1) > li:nth-child(1) > label > span"
        )
        condition_new.click()
        print("✅ 未使用フィルタを適用しました")
    except Exception as e:
        print(f"⚠️ フィルタが見つかりません。スキップします。({e})")

def get_href():
    """検索結果ページの全商品URLを取得"""
    href_list = []
    # 商品リンクのみ抽出
    href_elems = driver.find_elements(
        By.CSS_SELECTOR,
        "a.Product__titleLink"
    )
    for elem in href_elems:
        href = elem.get_attribute("href")
        if href not in href_list:
            href_list.append(href)
    print(f"🔗 商品リンク {len(href_list)} 件取得")
    return href_list


# -----------------------------------------
# 詳細ページ情報取得
# -----------------------------------------
def get_detail():
    """商品詳細ページからタイトル・価格などを取得"""
    wait_for_page_ready(driver)

    try:
        title_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#itemTitle > div > div > h1"))
        )
        title = title_elem.text.strip()
    except Exception as e:
        print("❌ タイトル要素が見つかりませんでした。スキップします。")
        print(f"  詳細: {e}")
        return

        # 現在のページURLを取得
    url = driver.current_url

    # 価格
    try:
        price_elem = driver.find_element(By.CSS_SELECTOR, "dl > dd > span.sc-1f0603b0-2")
        price = price_elem.text.strip()
    except:
        price = "不明"

    # 送料
    try:
        send_fee = driver.find_element(By.CSS_SELECTOR, "dl > dd > span.gv-u-fontSize16--_aSkEz8L_OSLLKFaubKB").text.strip()
    except:
        send_fee = "0"

    detail = {"タイトル": title, "価格": price, "送料": send_fee, "URL": url}
    detail_list.append(detail)
    print(f"✅ 詳細取得: {title}")


def get_photos():
    """商品ページの画像URLを全て取得"""
    wait_for_page_ready(driver)
    d_img = {}

    try:
        img_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img[src*='aucimg'], img.ProductImage__image"))
        )
        img = img_elem.get_attribute("src") or img_elem.get_attribute("data-src")
        d_img["picture_1"] = img
    except:
        print("⚠️ メイン画像が見つかりませんでした。スキップします。")
        return

    photo_elems = driver.find_elements(By.CSS_SELECTOR, "li.ProductImage__thumbnail")
    i = 2

    for photo_elem in photo_elems:
        try:
            photo_elem.click()
            time.sleep(1)
            img_elem = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.is-on img, img[src*='aucimg']"))
            )
            img = img_elem.get_attribute("src") or img_elem.get_attribute("data-src")
            d_img[f"picture_{i}"] = img
            i += 1
        except:
            print(f"⚠️ 画像 {i} の取得に失敗しました。")

    photo_list.append(d_img)
    print(f"📸 {len(d_img)} 枚の写真を取得しました。")


# -----------------------------------------
# メイン処理
# -----------------------------------------
def search(keyword):
    print(f"🔍 '{keyword}' を検索しています...")
    driver.get("https://auctions.yahoo.co.jp/")
    time.sleep(2)

    # 検索キーワード入力
    elm = driver.find_element(By.CSS_SELECTOR, "div > div > input")
    elm.send_keys(keyword)
    time.sleep(1)

    try:
        # ✅ JavaScriptで強制クリック（広告バナーを無視）
        search_button = driver.find_element(By.CSS_SELECTOR, "input#acHdSchBtn")
        driver.execute_script("arguments[0].click();", search_button)
        print("✅ 検索ボタンをクリックしました。")
    except Exception as e:
        print("⚠️ クリックに失敗したため Enter キーで検索します:", e)
        elm.send_keys(keys.Enter)

    time.sleep(3)
    wait_for_page_ready(driver)

    # 条件フィルタ
    condition()
    wait_for_page_ready(driver)

    # オークションタブへ移動
    #try:
    #    auction = driver.find_element(By.CSS_SELECTOR, "a.Tab__itemInner").get_attribute("href")
    #    driver.get(auction)
    #    wait_for_page_ready(driver)
    #except:
    #    print("⚠️ オークションタブに移動できませんでした。")

    # ページを一番下までスクロール
    scroll_to_bottom(driver)

    # 商品詳細収集
    hrefs = get_href()
    for href in hrefs:
        driver.get(href)
        time.sleep(2)
        # if "page.auctions.yahoo.co.jp" not in driver.current_url:
        #    print(f"⚠️ スキップ: 広告ページでした {href}")
        #    continue
        get_detail()
        # get_photos()

    # Excelに保存
    df_detail = pd.DataFrame(detail_list)
    df_photo = pd.DataFrame(photo_list)
    df_concat = pd.concat([df_detail, df_photo], axis=1)
    df_concat.to_excel("yahuoku_data.xlsx", index=False)
    print("💾 yahuoku_data.xlsx に保存しました。")


if __name__ == "__main__":
    search("基本情報技術者試験")
    driver.quit()
