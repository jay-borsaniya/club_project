from flask import request
from flask import current_app as app
from flask_restx import Resource, Namespace
from .service import AppConfig
from ..common import auth
from ...utils import err_resp

category = Namespace("AppConfig", description="AppConfig")

@category.route("/")
class AppConfig_Ns(Resource):

    def get(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )

        if request.args.get("id"):
            category_id = str(request.args.get("id"))
            if len(str(category_id)) != 0:
                return AppConfig.get_data(category_id)
        
        return AppConfig.get_all_data() 
