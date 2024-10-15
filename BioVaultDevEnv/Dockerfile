FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
FROM mysql:latest
ENV MYSQL_ROOT_PASSWORD="ilovelamp"
ENV MYSQL_DATABASE="biometric_auth"
COPY tablequeries.sql /docker-entrypoint-initdb.d/
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]