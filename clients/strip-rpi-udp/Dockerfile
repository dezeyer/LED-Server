FROM python:3.7.2-alpine3.9

RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk add --update --no-cache ca-certificates gcc g++ curl openblas-dev@community
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip install --no-cache-dir RPi.GPIO

WORKDIR /usr/src/rpi-udp-strip
COPY . /usr/src/rpi-udp-strip
CMD python3.7 -u /usr/src/rpi-udp-strip/rpi_udp_strip.py
