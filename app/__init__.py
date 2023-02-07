from flask import Flask
from pymongo import MongoClient
from .extensions import jwt, ma, mail

MONGO_URI = 'mongodb+srv://jay:Jay123@cluster0.nvj7by8.mongodb.net/?retryWrites=true&w=majority'
MONGO_DB = 'exercise'

def create_app():
    app = Flask(__name__)

    # register_extensions(app)

    client = MongoClient(MONGO_URI)
    app.db = client[str(MONGO_DB)]

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix="/")

    app.run(host='0.0.0.0', port=5000, debug=True)

def register_extensions(app):
    ma.init_app(app)
    # app.config.from_pyfile('../configuration.cfg')
    app.config['SECRET_KEY'] = "secret"
    app.config['MAIL_SERVER'] = "smtp.gmail.com"
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = "jayborsaniya.softrefine@gmail.com"
    app.config['MAIL_PASSWORD'] = "tjawfxxarwteltuf"
    app.config['MAIL_DEFAULT_SENDER'] = ("jay", "jayborsaniya.softrefine@gmail.com")
    app.config['MAIL_MAX_EMAILS'] = None
    app.config['MAIL_ASCII_ATTACHMENTS'] = False

    jwt.init_app(app)
    mail.init_app(app)

