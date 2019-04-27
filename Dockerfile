FROM python:3.7.2-alpine3.9

RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk add --update --no-cache ca-certificates gcc g++ curl openblas-dev@community
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

#COPY . .

#CMD [ "ls", "/usr/src/app/" ]
#CMD [ "python3.7", "/usr/src/app/LEDServer.py" ]
