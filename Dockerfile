FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Сделаем entrypoint.sh исполняемым
RUN chmod +x ./entrypoint.sh

# Откроем порт 8000 (если используем FastAPI/Uvicorn)
EXPOSE 8000

# Запуск через скрипт
ENTRYPOINT ["./entrypoint.sh"]

