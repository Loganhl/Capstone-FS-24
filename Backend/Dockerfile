FROM node:lts-alpine3.20
#set a work directory
WORKDIR /usr/src/app
COPY package-lock.json .
COPY package.json .
COPY server.js .
COPY biovault-backend.json .
COPY keycloak.json .
COPY ./middlewares ./middlewares

#install packages 
RUN npm install
#set the environment variables
# ENV KEYCLOAK_REALM="biovault"
# ENV KEYCLOAK_CLIENT="backend"
# ENV KEYCLOAK_CLIENT_SECRET=RKKfai8k9Kq78TGoG9vs9grohehNkTWg
# ENV SQL_PASS=secretsquirrels
# ENV SQL_HOST=mysql
# ENV SQL_PORT=3306
# ENV KEYCLOAK_URL=http://keycloak
# ENV SQL_DB=biometric_auth
# ENV SQL_USER=root
# ENV TOKEN_URL=http://keycloak:8080/realms/biovault/protocol/openid-connect/token
#expose 2500
EXPOSE 2500

ENTRYPOINT [ "npm start" ]