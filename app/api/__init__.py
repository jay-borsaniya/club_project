from flask_restx import Api
from flask import Blueprint

from .user.controller import admin as admin_ns
from .category.controller import category as category_ns
from .reservation.controller import reservation as reservation_ns
from .events.controller import events as events_ns
from .global_access.controller import globalaccess as globalaccess_ns

api_bp = Blueprint("api", __name__)

api = Api(api_bp, title="exercise project", description="exercise project for structure")

api.add_namespace(admin_ns)
api.add_namespace(category_ns)
api.add_namespace(reservation_ns)
api.add_namespace(events_ns)
api.add_namespace(globalaccess_ns)
