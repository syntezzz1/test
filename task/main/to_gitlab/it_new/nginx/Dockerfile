FROM nginx:1.24.0

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update &&\
    apt -y install --no-install-recommends \
        nano \
        vim-tiny &&\
    apt clean &&\
    rm -rf /var/lib/apt/lists/*

COPY default.conf /etc/nginx/conf.d/

CMD nginx -g 'daemon off;'
