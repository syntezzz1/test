# Запуск через docker compose

1. Собираем композ:

```
docker-compose build
```

2. Запускаем композ:

```
docker-compose up
```


# Запуск через Docker


1. Запускаем Postgres:
   
```
docker run \
--name star_postgres \
-p 5432:5432 \
-e POSTGRES_DB=mydatabase \
-e POSTGRES_USER=myuser \
-e POSTGRES_PASSWORD=mypassword \
-v /home/vstarkov/Pictures/MyPython/my-apps-docker/postgres_data:/var/lib/postgresql/data \
--detach=true \
--network host \
postgres:latest
```

2. Собираем образ Tasks:

```
docker build -t tasks_image tasks
```

3. Запускаем контейнер Tasks

```
docker run \
--name=star_tasks \
-p 5050:5050 \
--network host \
--detach=true \
tasks_image:latest
```

4. Собираем образ Worker:

```
docker build -t worker_image worker
```

5. Запускаем контейнер Worker:

```
docker run \
-p 5050:5050 \
--network host \
--name=star_worker \
--detach=true \
worker_image:latest
```


