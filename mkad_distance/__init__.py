from flask import Flask
from secrets import token_urlsafe

def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = token_urlsafe(16)

    from . import mkad_distance
    app.register_blueprint(mkad_distance.bp)

    return app