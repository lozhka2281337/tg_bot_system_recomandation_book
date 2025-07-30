FROM python:3.12.4

WORKDIR /workapp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV REDIS_HOST = "localhost"
ENV REPIS_PORT = "6379"

CMD ["python", "main.py"]


