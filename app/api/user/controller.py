from flask_restx import Resource, Namespace, Api
from flask import request, jsonify
from flask import current_app as app
from app.api.common import auth
from app.utils import err_resp, validation_error
from .service import AdminService, MemberService
from .utils import AdminSchema, AuthAdminSchema, AuthVerifyAdminSchema, MemberSchema

admin_schema = AdminSchema()
admin_auth_schema = AuthAdminSchema()
admin_auth_verify_schema = AuthVerifyAdminSchema()
member_schema = MemberSchema()

admin = Namespace("user", description="Admin CRUD Operations.")

@admin.route("/admin/")
class Admin(Resource):
    @admin.doc(params={'id': {'description': 'id', 'in': 'query', 'type': 'string'}})
    def get(self):
        result = {
            "status":200
        }
        return jsonify(result)
        # resp = auth.token_required(request.headers.get("Authorization"))
        # if resp["status"] != 200:
        #     return err_resp(
        #         resp["msg"],
        #         resp["msg"],
        #         resp["status"]
        #     )
        # id = request.args.get("id")
        # return AdminService.get_admin_data(id)

    def post(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        data = request.get_json()
        if (errors := admin_schema.validate(data)):
            return validation_error(False, errors), 400
        return AdminService.post_admin_data(data)

    def patch(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        data = request.get_json()
        return AdminService.patch_admin_data(data)

    def delete(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        id = request.args.get("id")
        return AdminService.delete_admin_data(id)

@admin.route("/admins/")
class Admins(Resource):
    @admin.doc(params={'id': {'description': 'id', 'in': 'query', 'type': 'string'}})
    def get(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        q = request.args.get("q", "")
        skip = request.args.get("skip", 0)
        limit = request.args.get("limit", 10)
        flag = request.args.get("flag", "0")
        return AdminService.get_all_admin_data(q, int(skip), int(limit), flag)

@admin.route("/member/")
class Member(Resource):
    @admin.doc(params={'id': {'description': 'id', 'in': 'query', 'type': 'string'}})
    def get(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        id = request.args.get("id")
        return MemberService.get_member_data(id)
    
    def post(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        data = request.get_json()
        if (errors := member_schema.validate(data)):
            return validation_error(False, errors), 400
        return MemberService.post_member_data(data)
    
    def patch(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        data = request.get_json()
        return MemberService.patch_member_data(data)

    def delete(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        id = request.args.get("id")
        return MemberService.delete_member_data(id)

@admin.route("/members/")
class Members(Resource):
    @admin.doc(params={'id': {'description': 'id', 'in': 'query', 'type': 'string'}})
    def get(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        q = request.args.get("q", "")
        skip = request.args.get("skip", 0)
        limit = request.args.get("limit", 0)
        return MemberService.get_all_member_data(q, int(skip), int(limit))


@admin.route("/admin/generateOtp")
class AdminAuthGenerateOtp(Resource):
    @admin.doc(params={'id': {'in': 'query', 'type': 'string'}})
    def post(self):
        data = request.get_json()
        if (errors := admin_auth_schema.validate(data)):
            return validation_error(False, errors), 400
        return AdminService.get_auth_admin(data)


@admin.route("/admin/verifyOtp")
class AdminVerifyOtp(Resource):
    @admin.doc(params={'id': {'description': 'id', 'in': 'query', 'type': 'string'}})
    def get(self):
        data = {
            "otpId": request.args.get("otpId"),
            "otpCode": request.args.get("otpCode"),
            "userType": request.args.get("userType")
        }
        if (errors := admin_auth_verify_schema.validate(data)):
            return validation_error(False, errors), 400
        return AdminService.get_verify_admin(data)


@admin.route("/member/generateOtp")
class MemberAuthGenerateOtp(Resource):
    @admin.doc(params={'id': {'in': 'query', 'type': 'string'}})
    def post(self):
        data = request.get_json()
        if (errors := admin_auth_schema.validate(data)):
            return validation_error(False, errors), 400
        return MemberService.get_auth_member(data)


@admin.route("/member/verifyOtp")
class MemberVerifyOtp(Resource):
    @admin.doc(params={'id': {'description': 'id', 'in': 'query', 'type': 'string'}})
    def get(self):
        data = {
            "otpId": request.args.get("otpId"),
            "otpCode": request.args.get("otpCode"),
            "userType": request.args.get("userType")
        }
        if (errors := admin_auth_verify_schema.validate(data)):
            return validation_error(False, errors), 400
        return MemberService.get_verify_member(data)

@admin.route("/admin/roles/")
class EditRoles(Resource):
    def patch(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        data = request.get_json()
        return AdminService.patch_role_data(data["users"])

