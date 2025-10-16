# ベースイメージ
FROM python:3.10-slim

# 必要パッケージのインストール
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl fonts-ipafont-gothic fonts-ipafont-mincho \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome のインストール（新しいキー管理方式に対応）
RUN mkdir -p /usr/share/keyrings \
    && wget -q -O /usr/share/keyrings/google-linux-signing-key.gpg https://dl.google.com/linux/linux_signing_key.pub \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 環境変数（Chrome設定）
ENV CHROME_ARGS="--no-sandbox --disable-dev-shm-usage --disable-gpu --disable-blink-features=AutomationControlled --remote-debugging-port=9222"

# 作業ディレクトリ
WORKDIR /app

# Python依存関係
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードコピー
COPY . .

# 実行
CMD ["python", "main.py"]
