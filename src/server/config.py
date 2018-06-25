import os

path = os.path.join(os.path.dirname(__file__), "prod_secret.txt")
try:
    with open(path, "r") as file_:
        prod_secret = file_.read().strip()
except FileNotFoundError as e:
    raise FileNotFoundError("Production secret file does not exist.") from e
if not prod_secret:
    raise ValueError("Production secret file is blank.")


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "asecret"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        "sqlite:////home/metamarcdw/python-fullstack-transcrypt/src/server/db.sqlite3"
    JWT_SECRET_KEY = prod_secret


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        r"sqlite:///C:\Users\cypher\Desktop\fullstack-react\todos_fs\src\server\db.sqlite3"


class TestingConfig(Config):
    TESTING = True
