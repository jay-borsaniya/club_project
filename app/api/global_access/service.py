from flask import current_app as app
from bson import ObjectId
from app.utils import err_resp, internal_err_resp, message
from app.api.common import validate

class GlobalAccessService:
    @staticmethod
    def post_data(data):
        try:
            app.db.globalAccess.insert_one(data)
            resp = message(True, "Data Inserted")
            resp["data"] = []
            return resp, 200

        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_data(id):
        try:
            if not validate.validateMongoId(id):
                resp = message(True, "Missing/Incorrect Objects Id")
                return resp, 422
            data = app.db.globalAccess.find_one({"_id": ObjectId(id)}, {"_id":0})

            if data:
                resp = message(True, "Success")
                resp["data"] = data
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
    def patch_data(data):
        try:
            id = data.get("id")
            if not validate.validateMongoId(id):
                resp = message(True, "Missing/Incorrect Object Id")
                return resp, 422
            adata = app.db.globalAccess.find_one({"_id": ObjectId(id)}, {"_id": 0})

            if adata:
                adata.update((k, data[k]) for k in (adata.keys() & data.keys()))
                app.db.globalAccess.update_one({"_id": ObjectId(id)}, {"$set": adata})
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
            
            data = app.db.globalAccess.find_one({"_id": ObjectId(id)})

            if data:
                app.db.globalAccess.delete_one({"_id": ObjectId(id)})
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
    def list_all(skip, limit, continent):
        try:
            final_data = []
            data = app.db.globalAccess.find({"continent": {'$regex': str(continent), '$options': 'i'}}).skip(skip).limit(limit)
            total_count = app.db.globalAccess.count_documents({"continent": {'$regex': str(continent), '$options': 'i'}})
            if total_count > 0:
                for i in data:
                    final_data.append({
                        "id": str(i["_id"]),
                        "name": i['name'],
                        "facilities": i["facilities"],
                        "benefits": i["benefits"],
                        "visits": i["visits"],
                        "country": i["country"],
                        "continent": i["continent"],
                        "location": i["location"],
                        "address": i["address"],
                        "recommendation": i["recommendation"],
                        "url": i["url"],
                        "clubLogos": i.get("clubLogos", []),
                        "clubPhotos": i.get("clubPhotos", []),
                        "clubMaps": i.get("clubMaps", []),
                    })
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
    def list_all_continents():
        try:
            data = app.db.globalAccess.distinct("continent")

            if data:
                resp = message(True, "Data Found")
                resp["data"] = data
                return resp, 200

            return err_resp(
                "Data Not Found",
                "Data Not Found",
                404
            )

        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()