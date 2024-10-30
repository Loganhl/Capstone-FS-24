FROM node:lts-alpine3.20

WORKDIR /frontend


COPY . /frontend/

COPY package.json /frontend/
COPY package-lock.json /frontend/
COPY . /frontend/

RUN npm install


