FROM python:3.12-slim

WORKDIR /app

# 安裝依賴
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式碼
COPY . .

# 設定環境變數
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# 建立必要的目錄
RUN mkdir -p instance migrations
RUN python init_db.py

# 暴露端口
EXPOSE 5000

# 啟動應用程式
CMD ["python", "run.py"]

