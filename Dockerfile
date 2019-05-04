FROM python:3.7.2-alpine3.9

RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk add --update --no-cache ca-certificates gcc g++ curl openblas-dev@community
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

WORKDIR /usr/src/LEDServer
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir numpy 
RUN pip3 install --no-cache-dir pylint 
RUN pip3 install --no-cache-dir RPi.GPIO 
RUN pip3 install --no-cache-dir --upgrade ptvsd 
# RUN pip3 install --no-cache-dir scipy # scipy is only required by the recorder application

