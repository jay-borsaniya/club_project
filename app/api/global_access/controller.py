from flask import current_app as app, request
from flask_restx import Resource, Namespace
from app.utils import validation_error, err_resp 
from app.api.common import auth
from .utils import GlobalAccess
from .service import GlobalAccessService

global_schema = GlobalAccess()

globalaccess = Namespace("globalaccess", description="GlobalAccess CRUD operations")

@globalaccess.route("/")
class global_access(Resource):
    def post(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        data = request.get_json()
        if (errors := global_schema.validate(data)):
            return validation_error(False, errors), 400
        return GlobalAccessService.post_data(data)

    def get(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        id = request.args.get("id")
        return GlobalAccessService.get_data(id)

    def patch(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        data = request.get_json()
        return GlobalAccessService.patch_data(data)

    def delete(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        id = request.args.get("id")
        return GlobalAccessService.delete_data(id)

@globalaccess.route("/list")
class global_access_list(Resource):

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
        continent = request.args.get("continent", "")

        return GlobalAccessService.list_all(int(skip), int(limit), continent)

@globalaccess.route("/list/continents")
class global_access_list_continents(Resource):

    def get(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        return GlobalAccessService.list_all_continents()