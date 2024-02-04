# Как посмотреть размер образа?
# Нужно уменьшить суммарный размер образов основанных на debian, какие есть пути решения?
# Нужно уменьшить размер каждого образа, какие есть пути решения?
FROM debian:bookworm-backports

ARG DEBIAN_FRONTEND=noninteractive

LABEL maintainer="v.pukin@test.ru"

# Линтер ругается на строку ниже, хотя она работает. Что может быть не так?
RUN apt update &&\
    apt -y install --no-install-recommends \
        apache2 \
        nano \
        vim-tiny &&\
    apt clean &&\
    rm -rf /var/lib/apt/lists/*

# Чем отличаются ENV от ARG?
ENV APACHE_RUN_USER www-data
# Как перенести переменные отсюда в .env?
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_RUN_DIR /usr/sbin/
ENV APACHE_PID_FILE /tmp/apache.pid

CMD ["apache2", "-D", "FOREGROUND"]
