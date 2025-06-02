FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Обновляем pip и ставим зависимости с очисткой кеша
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt

# Проверяем, что python-dotenv установлен
RUN pip show python-dotenv

COPY . .

CMD ["python", "copernicus_bot_v5_FINAL.py"]
