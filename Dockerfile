FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install python-dotenv==1.0.1 && \
    pip list

COPY . .

CMD ["python", "copernicus_bot_v5_FINAL.py"]
