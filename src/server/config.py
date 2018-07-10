import os
import sys
import json

secret_path = os.path.join(os.path.dirname(__file__), "prod_secrets.json")
try:
    with open(secret_path, "r") as file_:
        prod_secrets = json.load(file_)
except FileNotFoundError as e:
    raise FileNotFoundError(
        "\n * Production secret file:" +
        f"\n\tC{secret_path[1:]}\n   does not exist.") from e

keys = ("jwt_secret", "db_pswd", "mail_pswd")
if not prod_secrets or not all([key in prod_secrets for key in keys]):
    raise ValueError(
        "\n * Production secret file:" +
        f"\n\tC{secret_path[1:]}\n   is not complete.")

tempdir = os.environ["TMP"] if sys.platform == "win32" else "/tmp"


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "asecret"


class ProductionConfig(Config):
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USERNAME = "todos.fs.mailer"
    MAIL_PASSWORD = prod_secrets["mail_pswd"]
    ADMINS = ["marcdw87@gmail.com"]

    db_user = "metamarcdw"
    db_pswd = prod_secrets["db_pswd"]
    db_host = "metamarcdw.mysql.pythonanywhere-services.com"
    db_name = "todos_fs"
    SQLALCHEMY_DATABASE_URI = \
        f"mysql://{db_user}:{db_pswd}@{db_host}/{db_user}${db_name}"

    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 280
    JWT_SECRET_KEY = prod_secrets["jwt_secret"]


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        r"sqlite:///C:\Users\cypher\Desktop\fullstack-react\todos_fs\src\server\db.sqlite3"


class TestingConfig(Config):
    TESTING = True
    DB_PATH = os.path.join(tempdir, 'todos_fs.sqlite3')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
