from __future__ import annotations

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import logging
import os


mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_host = os.getenv("MYSQL_HOST")
mysql_port = os.getenv("MYSQL_PORT")
mysql_url = (
  f"mysql+mysqldb://{mysql_user}:{mysql_password}"
  f"@{mysql_host}:{mysql_port}/t3")

app_file = os.getenv("FLASK_APP")
assert app_file

app = Flask(app_file.strip(".py"))
app.config["SQLALCHEMY_DATABASE_URI"] = mysql_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
