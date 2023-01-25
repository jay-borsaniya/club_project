from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_mail import Mail

jwt = JWTManager()
ma = Marshmallow()
mail = Mail()