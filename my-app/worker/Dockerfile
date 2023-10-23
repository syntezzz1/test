# Dockerfile для сервиса tasks
FROM python:3.11-slim

WORKDIR /app

COPY ./worker.py /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["uvicorn", "worker:worker_app", "--host", "0.0.0.0", "--port", "5051"]
