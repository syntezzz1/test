# Dockerfile для сервиса tasks
FROM python:3.11-slim

WORKDIR /app

COPY ./tasks.py /app/
COPY requirements.txt /app/
COPY config.conf /app/

RUN pip install -r requirements.txt

CMD ["uvicorn", "tasks:task_app", "--host", "0.0.0.0", "--port", "5050"]
