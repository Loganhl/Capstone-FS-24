FROM node:lts-alpine3.20

WORKDIR /backend

COPY ./package.json .
COPY ./db/ ./db
COPY ./middlewares/ ./middlewares
COPY ./package-lock.json .
COPY ./server.js .

RUN npm i