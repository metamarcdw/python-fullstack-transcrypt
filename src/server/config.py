import prod_secret

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "asecret"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        "sqlite:////home/metamarcdw/python-fullstack-transcrypt/src/server/db.sqlite3"
    JWT_SECRET_KEY = prod_secret.jwt_key

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        r"sqlite:///C:\Users\cypher\Desktop\fullstack-react\todos_fs\src\server\db.sqlite3"

class TestingConfig(Config):
    TESTING = True
