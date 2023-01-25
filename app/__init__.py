from flask import Flask
from pymongo import MongoClient
from .extensions import jwt, ma, mail
from .. import configuration 

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
    # app.config.from_pyfile('../configuration.cfg')
    app.config['SECRET_KEY'] = configuration.SECRET_KEY
    app.config['MAIL_SERVER'] = configuration.MAIL_SERVER
    app.config['MAIL_PORT'] = configuration.MAIL_PORT
    app.config['MAIL_USE_TLS'] = configuration.MAIL_USE_TLS
    app.config['MAIL_USE_SSL'] = configuration.MAIL_USE_SSL
    app.config['MAIL_USERNAME'] = configuration.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = configuration.MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = configuration.MAIL_DEFAULT_SENDER
    app.config['MAIL_MAX_EMAILS'] = configuration.MAIL_MAX_EMAILS
    app.config['MAIL_ASCII_ATTACHMENTS'] = configuration.MAIL_ASCII_ATTACHMENTS

    jwt.init_app(app)
    mail.init_app(app)

