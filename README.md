# 🪙 Yahoo!オークション スクレイピングツール

Yahoo!オークションで特定のキーワードを検索し、  
商品タイトル・価格・送料・URL を自動取得して Excel に保存する Python + Selenium ツールです。  
Docker で実行できるため、ローカル環境構築は不要です。

---

## 🚀 機能概要

- 指定キーワードで Yahoo!オークションを検索
- 「未使用」商品のみを抽出
- 各商品の詳細ページから以下を取得  
  - タイトル  
  - 価格  
  - 送料  
  - 商品URL
- 取得結果を `yahuoku_data.xlsx` に自動保存
- Docker で簡単実行

---

## 🧩 構成
```
yahoo_auctions_scraping/
├── main.py # メインスクリプト
├── Dockerfile # 実行環境構築用
├── requirements.txt # Python依存パッケージ
├── .gitignore
└── README.md
```

---

## 🐳 実行方法

### 1. イメージをビルド

```bash
docker build -t selenium-yahuoku .
```
2. スクリプトを実行
```bash
コードをコピーする
docker run --rm -v "${PWD}:/app" selenium-yahuoku
```
3. 結果の確認
完了後、カレントディレクトリに以下が出力されます：
yahuoku_data.xlsx

## 🧠 ヒント
スクロール処理で全商品を読み込むよう対応済み。

取得件数は div.Option--count > button > span.Option__selected から確認。

実行ログで「✅」「⚠️」などが表示され、進行状況を把握できます。

🪄 開発者向けメモ
ローカル実行（開発用）
```bash
pip install -r requirements.txt
python main.py
```
注意点
Yahoo!オークションのDOM構造は変更される可能性があります。
要素の CSSセレクタ は適宜更新してください。

ブラウザ操作には時間がかかるため、WebDriverWait を活用して安定化しています。

📝 ライセンス
MIT License

---