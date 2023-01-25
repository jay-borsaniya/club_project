from flask import request
from flask_restx import Resource, Namespace

from .service import EventService
from .utils import EventSchema
from app.utils import err_resp, validation_error
from app.api.common import auth

event_schema = EventSchema()

events = Namespace("events", description="Event CRUD Operations")

@events.route("/")
class Event(Resource):

    def post(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        
        data = request.get_json()
        if (errors := event_schema.validate(data)):
            return validation_error(False, errors), 400
        return EventService.post_data(data)
    
    def get(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        
        id = request.args.get("id")
        return EventService.get_data(id)

    def patch(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        data = request.get_json()
        return EventService.patch_data(data)

    def delete(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        id = request.args.get("id")
        return EventService.delete_data(id)


@events.route("/list")
class Events(Resource):
    def get(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        skip = request.args.get("skip", 0)
        limit = request.args.get("limit", 10)
        return EventService.list_all(int(skip), int(limit))

@events.route("/categories")
class EventsCategories(Resource):
    def get(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        return EventService.list_all_categories()
