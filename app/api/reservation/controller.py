from flask import current_app as app
from flask_restx import Resource, Namespace
from flask import request
from ..common import auth
from ...utils import validation_error, err_resp
from .utils import ReservationSchema
from .service import ReservationService

reservation_schema = ReservationSchema()

reservation = Namespace("reservation", description="reservation CRUD operations")


@reservation.route('/')
class Reservation(Resource):
    def post(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        data = request.get_json()
        if (errors := reservation_schema.validate(data)):
            return validation_error(False, errors), 400
        return ReservationService.post_data(data)

    def get(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        id = request.args.get("id")
        return ReservationService.get_data(id)

    def patch(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        data = request.get_json()
        return ReservationService.patch_data(data)

    def delete(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        id = request.args.get("id")
        return ReservationService.delete_data(id)


@reservation.route('/list')
class Reservations(Resource):
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
        date = request.args.get("date")
        q = request.args.get("q", "")
        area = request.args.get("area", "")

        return ReservationService.list_all(int(skip), int(limit), date, q, area)


@reservation.route('/reservation_download')
class Reservation_download(Resource):
    def get(self):
        resp = auth.token_required(request.headers.get("Authorization"))
        if resp["status"] != 200:
            return err_resp(
                resp["msg"],
                resp["msg"],
                resp["status"]
            )
        id = request.args.get("id")
        return ReservationService.download_receipt(id)