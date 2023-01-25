from flask import current_app as app
from ...utils import err_resp, message, internal_err_resp
from bson import ObjectId
class AppConfig:

    @staticmethod
    def get_data(id):
        try:
            data = app.db.category.find_one({"_id": ObjectId(id)})
            if data:
                resp = message(True, "Sub Category Found")
                resp["data"] = data["category"]
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
    def get_all_data():
        try:
            data = app.db.category.find({})
            if data:
                resp = message(True, "Category Found")
                result = []
                res = {}
                for i in data:
                    res["id"] = str(i["_id"])
                    res["name"] = str(i["name"])
                    result.append(res)

                resp["data"] = result
                return resp, 200
            
            return err_resp(
                "Data Not Found",
                "Data Not Found",
                404
            )
        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()
