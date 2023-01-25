from flask import current_app as app, send_file
from ..common import validate
from bson import ObjectId
from ...utils import err_resp, message, internal_err_resp
import json

class ReservationService:
    @staticmethod
    def post_data(data):
        try:
            data["isApproved"] = False
            app.db.reservation.insert_one(data)
            resp = message(True, "Reservation Complete")
            reservation_data = app.db.reservation.find_one({"memberId":data["memberId"]})
            reservation_id = str(reservation_data["_id"])
            print(reservation_id)
            resp["data"] = []
            resp["reservation_id"] = reservation_id

            return resp, 200
        
        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_data(id):
        try:
            if not validate.validateMongoId(id):
                resp = message(True, "Missing/Incorrect Object Id")
                return resp, 422
            data = app.db.reservation.find_one({"_id": ObjectId(id)})
            data["_id"] = str(data["_id"])
            if data:
                resp = message(True, "Data Found")
                resp["data"] = data
                return resp, 200

            return err_resp(
                "Data Not Found.",
                "Data Not Found",
                404
            )
        
        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()
    
    @staticmethod
    def patch_data(data):
        try:
            id = data.get("id")
            if not validate.validateMongoId(id):
                resp = message(True, "Missing/Incorrect Object Id")
                return resp, 422
            adata = app.db.reservation.find_one({"_id": ObjectId(id)}, {"_id": 0})

            if adata:
                adata.update((k, data[k]) for k in (adata.keys() & data.keys()))
                app.db.reservation.update_one({"_id": ObjectId(id)}, {"$set": adata})
                resp = message(True, "Data Updated")
                resp["data"] = []
                return resp, 200

            return err_resp(
                "Data Not Found",
                "Data Not Found",
                404
            )

        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def delete_data(id):
        try:
            if not validate.validateMongoId(id):
                resp = message(True, "Missing/Incorrect Object Id")
                return resp, 422
            
            data = app.db.reservation.find_one({"_id": ObjectId(id)})

            if data:
                app.db.reservation.delete_one({"_id": ObjectId(id)})
                resp = message(True, "Data Deleted")
                resp["data"] = []
                return resp, 200
            
            return err_resp(
                "Data Not Found",
                "Data Not Found",
                404
            )

        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def list_all(skip, limit, date, q, area):
        try:
            final_data = []
            query = {}

            if date:
                query["date"] = str(date)
            
            if str(q) != "":
                query["$or"] = [
                    {"memberId": {'$regex': str(q), '$options': 'i'}},
                    {"member": {'$regex': str(q), '$options': 'i'}}
                ]
            
            if str(area) != "":
                query["$or"] = [
                    {"area": {'$regex': str(area), '$options': 'i'}}
                ]
            
            data = app.db.reservation.find(query).skip(skip).limit(limit)
            total_count = app.db.reservation.count_documents(query)

            if total_count > 0:
                for i in data:
                    i["id"] = str(i["_id"])
                    del i["_id"]
                    final_data.append(i)
                resp = message(True, "Data Found")
                resp["data"] = final_data
                resp["total_count"] = total_count
                return resp, 200
            
            return err_resp(
                "Data Not Found",
                "Data Not Found",
                404
            )
        
        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def download_receipt(id):
        try:
            if not validate.validateMongoId(id):
                resp = message(True, "Missing/Incorrect Object Id")
                return resp, 422
            

            data = app.db.reservation.find_one({"_id": ObjectId(id)})

            if data:
                file_name = "{}.csv".format(id)
                data["_id"] = str(data["_id"])
                result = dict(data)
                final_data = []
                final_data.append(result)
                print(final_data)
                with open(file_name, 'w', newline='') as f:
                    f.write(json.dumps(final_data))
                    # return file_name
                    return result
                    # return send_file('../{}'.format(file_name), as_attachment=True)

            return err_resp(
                "Data Not Found",
                "Data Not Found",
                404
            )

        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()



