from flask import Flask
from pymongo import MongoClient
from .extensions import jwt, ma, mail

MONGO_URI = 'mongodb+srv://jay:Jay123@cluster0.nvj7by8.mongodb.net/?retryWrites=true&w=majority'
MONGO_DB = 'exercise'

def create_app():
    app = Flask(__name__)

    register_extensions(app)

    client = MongoClient(MONGO_URI)
    app.db = client[str(MONGO_DB)]

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix="/")

    app.run(host='0.0.0.0', debug=True)

def register_extensions(app):
    ma.init_app(app)
    app.config.from_pyfile('../configuration.cfg')
    jwt.init_app(app)
    mail.init_app(app)

