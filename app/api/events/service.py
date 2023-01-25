from flask import current_app as app
from bson import ObjectId

from app.utils import err_resp, message, internal_err_resp
from app.api.common import validate

class EventService:
    @staticmethod
    def post_data(data):
        try:
            app.db.events.insert_one(data)
            resp = message(True, "Data Inserted")
            resp["data"] = []
            return resp, 201

        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()
    

    @staticmethod
    def get_data(id):
        try:
            if not validate.validateMongoId(id):
                resp = message(True, "Missing/Incorrect Object Id")
                return resp, 422
            data = app.db.events.find_one({"_id": ObjectId(id)}, {"_id":0})

            if data:
                resp = message(True, "success")
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
            adata = app.db.events.find_one({"_id": ObjectId(id)}, {"_id":0})

            if adata:
                adata.update((k, data[k]) for k in (adata.keys() & data.keys()))
                app.db.events.update_one({"_id": ObjectId(id)}, {"$set": adata})
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
            return  internal_err_resp()

    @staticmethod
    def delete_data(id):
        try:
            if not validate.validateMongoId(id):
                resp = message(True, "Missing/Incorrect Object_id")
                return resp, 422
            
            data = app.db.events.find_one({"_id": ObjectId(id)})
            if data:
                app.db.events.delete_one({"_id": ObjectId(id)})
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
    def list_all(skip, limit):
        try: 
            final_data = []
            data = app.db.events.find({}).skip(skip).limit(limit)
            total_count = app.db.events.count_documents({})

            if total_count > 0:
                for i in data:
                    final_data.append({
                        "id": str(i["_id"]),
                        "eventTitle": i["eventTitle"],
                        "isMembersOnly": i["isMembersOnly"],
                        "eventDate": i["eventDate"],
                        "eventTime": i["eventTime"],
                        "eventNature": i["eventNature"],
                        "eventAbout": i["eventAbout"],
                        "eventVenue": i["eventVenue"],
                        "eventImage": i["eventImage"],
                        "attendees": i["attendees"]
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
    def list_all_categories():
        try: 
            final_data = []
            data = app.db.events.distinct("eventNature")
            total_count = app.db.events.count_documents({})

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



