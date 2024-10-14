FROM node:latest

WORKDIR /frontend


COPY /public /frontend/

COPY /src /frontend/
COPY package.json /frontend/

RUN npm install

CMD ["npm", "start"]
