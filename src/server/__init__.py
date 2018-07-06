import os

from flask import Flask
from flask_restplus import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

authorizations = {
    "bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    },
    "basic": {
        "type": "basic"
    }
}

cors_resources = {
    r"/*": {
        "origins": [
            "https://metamarcdw.github.io",
            "http://localhost:3000"
        ],
        "supports_credentials": True
    }
}

api = Api(authorizations=authorizations)
cors = CORS(resources=cors_resources)

db = SQLAlchemy()
jwt = JWTManager()
jwt._set_error_handler_callbacks(api)
# https://github.com/vimalloc/flask-jwt-extended/issues/83


def create_app():
    mode = os.environ.get("TODOS_FS_MODE")
    config_type = None

    # Specifying the 'server' module is needed when run indirectly
    if mode == "production":
        config_type = "server.config.ProductionConfig"
    elif mode == "development":
        config_type = "server.config.DevelopmentConfig"
    elif mode == "testing":
        config_type = "server.config.TestingConfig"
    else:
        raise ValueError("Mode variable not set.")
    print(f" * Running the API in {mode} mode.")

    app = Flask(__name__)
    app.config.from_object(config_type)

    api.init_app(app)
    cors.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run()
