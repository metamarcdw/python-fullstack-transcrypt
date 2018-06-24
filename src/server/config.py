import os

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "asecret"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        "sqlite:////home/metamarcdw/python-fullstack-transcrypt/src/server/db.sqlite3"

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "prod_secret.txt")
        with open(path, "r") as file_:
            self.JWT_SECRET_KEY = file_.read().strip()

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        r"sqlite:///C:\Users\cypher\Desktop\fullstack-react\todos_fs\src\server\db.sqlite3"

class TestingConfig(Config):
    TESTING = True
