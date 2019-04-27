FROM nginx:stable-alpine

RUN apk add --update nodejs nodejs-npm

COPY . /usr/share/nginx/html

RUN cd /usr/share/nginx/html && npm install
