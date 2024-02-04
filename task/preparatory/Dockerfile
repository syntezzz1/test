FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    cmake

WORKDIR /app
COPY . /app

RUN mkdir build && cd build && \
    cmake ../ && \
    make -j10 && \
    make install

CMD ["./app"]
