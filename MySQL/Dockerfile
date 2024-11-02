FROM mysql:latest
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=mydb
ENV MYSQL_PASSWORD=pass
COPY ./scripts/ /docker-entrypoint-initdb.d/
