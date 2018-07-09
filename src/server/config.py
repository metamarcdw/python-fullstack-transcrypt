import os
import sys

secret_path = os.path.join(os.path.dirname(__file__), "prod_secret.txt")
try:
    with open(secret_path, "r") as file_:
        prod_secret = file_.read().strip()
except FileNotFoundError as e:
    raise FileNotFoundError(
        "\n * Production secret file:" +
        f"\n\tC{secret_path[1:]}\n   does not exist.") from e
if not prod_secret:
    raise ValueError(
        "\n * Production secret file:" +
        f"\n\tC{secret_path[1:]}\n   is blank.")

tempdir = os.environ["TMP"] if sys.platform == "win32" else "/tmp"


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "asecret"


class ProductionConfig(Config):
    user = "metamarcdw"
    pswd = "QxRTieF7NYYz8p6f"
    db_host = "metamarcdw.mysql.pythonanywhere-services.com"
    db_name = "todos_fs"
    SQLALCHEMY_DATABASE_URI = \
        f"mysql://{user}:{pswd}@{db_host}/{user}${db_name}"

    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 280
    JWT_SECRET_KEY = prod_secret


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        r"sqlite:///C:\Users\cypher\Desktop\fullstack-react\todos_fs\src\server\db.sqlite3"


class TestingConfig(Config):
    TESTING = True
    DB_PATH = os.path.join(tempdir, 'todos_fs.sqlite3')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
