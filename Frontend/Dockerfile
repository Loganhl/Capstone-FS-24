FROM node:lts-alpine3.20

WORKDIR /frontend


COPY /public /frontend/

COPY /src /frontend/
COPY package.json /frontend/
COPY package-lock.json /frontend/
RUN npm install


