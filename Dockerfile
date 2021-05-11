FROM python:3.9-alpine
WORKDIR /usr/src/app
RUN apk update && apk add ca-certificates build-base mariadb-client mariadb-dev
RUN pip install --upgrade pip
RUN pip install flask flask-sqlalchemy mysqlclient flask-migrate
RUN pip install requests
COPY . .
CMD ["python", "web.py"]
EXPOSE 5000