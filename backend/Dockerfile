FROM python:3.14-rc-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
CMD ["python3", "main.py"]
