FROM node:lts-alpine3.20
#set a work directory
WORKDIR /usr/src/app
COPY package-lock.json .
COPY package.json .
COPY server.js .
COPY biovault-backend.json .

#install packages 
RUN npm install

#expose 2500
EXPOSE 2500

ENTRYPOINT [ "npm start" ]