from flask import current_app as app
from app.utils import err_resp, message, internal_err_resp
from app.api.common import auth, validate
from app.api.library import sms, email
from bson import ObjectId
from random import randint
import time


class AdminService:

    @staticmethod
    def get_verify_admin(data):
        otpData = app.db.verificationCode.find_one({"_id":ObjectId(data.get("otpId"))})
        if not otpData:
            return err_resp(
                    "not valid otpId",
                    "check your otp id",
                    400
                )
        if otpData['expireAt'] < int(time.time()):
            return err_resp(
                    "otp code expire",
                    "check your otp code is expire",
                    400
                )
        if otpData['attempt'] > 3:
            return err_resp(
                    "attempt maximum limit reached",
                    "attempt maximum limit reached",
                    400
                )
        if str(data.get("otpCode")) != str(otpData['otp']):
            count = otpData['attempt'] + 1
            app.db.verificationCode.update_one({"_id":ObjectId(data.get("otpId"))},{'$set':{"attempt":count}})
            return err_resp(
                    "Invalid otp code",
                    "check your otp code",
                    400
                )
        if otpData['verified']==True:
            return err_resp(
                    "already verified otp code",
                    "already verified otp code",
                    400
                )

        final_data = {}
        if str(data["userType"]) == 'admin':
            admin_data = app.db.admins.find_one({"_id":ObjectId(otpData['userId'])})
            if admin_data:
                final_data = {
                    "id": str(admin_data["_id"]),
                    "imageUrl": admin_data["imageUrl"],
                    "gender": admin_data["gender"],
                    "title": admin_data["title"],
                    "firstName": admin_data["firstName"],
                    "middleName": admin_data["middleName"],
                    "lastName": admin_data["lastName"],
                    "dob": admin_data["dob"],
                    "email": admin_data["email"],
                    "phoneNo": admin_data["phoneNo"],
                    "address": admin_data["address"],
                    "roleTitle": admin_data["roleTitle"],
                    "clearanceLevel": admin_data["clearanceLevel"],
                    "joinDate": admin_data["joinDate"],
                    "clubs": admin_data["clubs"],
                    "isActive": admin_data["isActive"],
                    "adminRoles": admin_data["adminRoles"]
                }
                app.db.verificationCode.update_one({"_id":ObjectId(data.get("otpId"))},{'$set':{"verified":True}})
                resp = {}
                resp["data"] = final_data
                resp["tokens"] = auth.encodeAccessToken(otpData['userId'],"admin",admin_data["adminRoles"],{})
                return resp, 200
            else:
                return err_resp(
                    "Admin User Not Found",
                    "admin_404",
                    404
                )

        else:
            return err_resp(
                    "Please Check UserType",
                    "Invalid UserType",
                    400
                )

    @staticmethod
    def get_auth_admin(data):

        if str(data["userType"]) == 'admin': 
            admin_data = app.db.admins.find_one({"$or":[{'phoneNo': data.get("data")},{'email':data.get("data")}]})
            if not admin_data:
                return err_resp(
                    "admin user not found",
                    "user not found",
                    404
                )
        
        else:
            return err_resp(
                    "Please Check UserType",
                    "Invalid UserType",
                    400
                )

        otp = randint(100000, 999999)
        sms_msg = """Your One Time Password is : {} , Please Keep This Code Private"""

        if data.get("mode") == "phone":
            res = sms.send_sms(data.get("data"), sms_msg.format(str(otp)))

        if data.get("mode") == "email":
            res = email.send_email(data.get("data"), sms_msg.format(str(otp)))

        if res['status']:
            otpData={
                    'otp':otp,
                    'createdAt':int(time.time()),
                    'expireAt' : int(time.time()) + 6000,
                    # 'userId':str(admin_data['_id']),
                    'verified':False,
                    'attempt':1
                }

            if str(data["userType"]) == 'admin':
                otpData["userId"] = str(admin_data['_id'])

            app.db.verificationCode.delete_one({"userId": otpData["userId"]})
            app.db.verificationCode.insert_one(otpData)
            otp_data = app.db.verificationCode.find_one({"userId": otpData["userId"]})
            otpId = otp_data['_id']

            resp={}
            resp['otpId']=str(otpId)
            resp["message"]="OK"
            return resp, 200

        return err_resp(
                    "failed to send otp try again",
                    "error while sending otp",
                    419
                )

    @staticmethod
    def post_admin_data(data):
        access_payload = {
            "checkIn": 1,
            "reservations": 1,
            "guestCheckIn": 1,
            "events": 1,
            "newAtTheQ": 1,
            "globalAccess": 1,
            "anIndiaOfIdeas": 1,
            "AQ": 1,
            "editMember": 1,
            "adminRoles": 1
        }

        final_data = {
            "imageUrl": data.get("imageUrl"),
            "gender": data.get("gender"),
            "title": data.get("title"),
            "firstName": data.get("firstName"),
            "middleName": data.get("middleName"),
            "lastName": data.get("lastName"),
            "dob": data.get("dob"),
            "email": data.get("email"),
            "phoneNo": data.get("phoneNo"),
            "address": data.get("address"),
            "roleTitle": data.get("roleTitle"),
            "clearanceLevel": data.get("clearanceLevel"),
            "joinDate": data.get("joinDate"),
            "clubs": data.get("clubs"),
            "isActive": data.get("isActive", True),
            "adminRoles": access_payload,
            "notes": data.get("notes", "")
        }

        admin_data = app.db.admins.find_one({"phoneNo": final_data["phoneNo"]}, {"_id":0})
        if admin_data:
            return err_resp(
                "Monile Number Already Registerd.",
                "admin_409", 
                409
            )
        app.db.admins.insert_one(final_data)
        resp = message(True, "Admin Data Inserted")
        resp["data"] = []
        return resp, 201

    @staticmethod
    def get_admin_data(id):
        try:
            final_data = {}
            if not validate.validateMongoId(id):
                resp = message(True, "Missing/Incorrect Object Id")
                return resp, 422
            admin_data = app.db.admins.find_one({"_id": ObjectId(id)})
            if admin_data:
                final_data = {
                    "id": str(admin_data["_id"]),
                    "imageUrl": admin_data["imageUrl"],
                    "gender": admin_data["gender"],
                    "title": admin_data["title"],
                    "firstName": admin_data["firstName"],
                    "middleName": admin_data["middleName"],
                    "lastName": admin_data["lastName"],
                    "dob": admin_data["dob"],
                    "email": admin_data["email"],
                    "phoneNo": admin_data["phoneNo"],
                    "address": admin_data["address"],
                    "roleTitle": admin_data["roleTitle"],
                    "clearanceLevel": admin_data["clearanceLevel"],
                    "joinDate": admin_data["joinDate"],
                    "clubs": admin_data["clubs"],
                    "isActive": admin_data["isActive"],
                    "adminRoles": admin_data["adminRoles"],
                    "notes": admin_data.get("notes", "")
                }
                resp = message(True, "Admin data found")
                resp["data"] = final_data
                return resp, 200
            
            return err_resp(
                "Admin User Not Found.",
                "admin_404",
                404
            )
        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def patch_admin_data(data):
        id = data.get("id")
        if not validate.validateMongoId(id):
            resp = message(True, "Missing/Incorrect Object Id")
            return resp, 422
        admin_data = app.db.admins.find_one({"_id": ObjectId(id)}, {"_id": 0})
        if admin_data:
            admin_data.update((k, data[k]) for k in (admin_data.keys() & data.keys()))
            app.db.admins.update_one({"_id": ObjectId(id)},{"$set": admin_data})
            resp = message(True, "Admin data updated")
            resp["data"] = []
            return resp, 200

        return err_resp(
            "Admin User Not Found.",
            "admin_404",
            404
        )

    @staticmethod
    def delete_admin_data(id):
        try:
            if not validate.validateMongoId(id):
                resp = message(True, "Missing/Incorrect Object Id")
                return resp, 422

            admin_data = app.db.admins.find_one({"_id": ObjectId(id)})
            if admin_data:
                app.db.admins.delete_one({"_id": ObjectId(id)})
                resp = message(True, "Admin data deleted")
                resp["data"] = []
                return resp, 200
            
            return err_resp(
                "Admin User Not Found.",
                "admin_404",
                404
            )
        
        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_all_admin_data(q, skip, limit, flag):
        final_data = []
        query = {}
        if len(str(q)) != 0:
            query["$or"] = [
                {"firstName": {'$regex': str(q), '$options': 'i'}},
                {"lastName": {'$regex': str(q), '$options': 'i'}},
                {"middleName": {'$regex': str(q), '$options': 'i'}},
                {"email": {'$regex': str(q), '$options': 'i'}},
                {"phoneNo": {'$regex': str(q), '$options': 'i'}}
            ]
        if str(flag) == "1":
            query["isActive"] = True

        admin_data = app.db.admins.find(query).skip(skip).limit(limit)
        total_count = app.db.admins.count_documents(query)

        if total_count > 0:
            for i in admin_data:
                payload = {
                    "id": str(i["_id"]),
                    "imageUrl": i["imageUrl"],
                    "firstName": i["firstName"],
                    "middleName": i["middleName"],
                    "lastName": i["lastName"]
                }
                if str(flag) == "1":
                    payload["adminRoles"] = i["adminRoles"]
                    payload["isActive"] = i["isActive"]
                final_data.append(payload)
            resp = message(True, "Admin users found")
            resp["data"] = final_data
            resp["totalCount"] = total_count
            return resp, 200

        return err_resp(
            "Admin User Not Found",
            "admin_404",
            404
        )
    
    @staticmethod
    def patch_role_data(data):
        for i in data:
            app.db.admins.update_one({"_id": ObjectId(i["id"])},{"$set":{"adminRoles": i["adminRoles"]}})

        resp = message(True, "Admin Roles Updated")
        resp["data"] = []
        return resp, 200


class MemberService:

    @staticmethod
    def get_member_data(id):
        final_data = {}
        if not validate.validateMongoId(id):
            resp = message(True, "Missing/Incorrect Object Id")
            return resp, 422
        member_data = app.db.members.find_one({"_id": ObjectId(id)})
        if member_data:
            final_data = {
                "id": str(member_data["_id"]),
                "imageUrl": member_data["imageUrl"],
                "gender": member_data["gender"],
                "title": member_data["title"],
                "firstName": member_data["firstName"],
                "middleName": member_data["middleName"],
                "lastName": member_data["lastName"],
                "dob": member_data["dob"],
                "email": member_data["email"],
                "phoneNo": member_data["phoneNo"],
                "address": member_data["address"],
                "company": member_data["company"],
                "industry": member_data["industry"],
                "jobTitle": member_data["jobTitle"],
                "mNo": member_data["mNo"],
                "mType":member_data["mType"],
                "startDate": member_data["startDate"],
                "endDate": member_data["endDate"],
                "acType": member_data["acType"],
                "acFName": member_data["acFName"],
                "acLName": member_data["acLName"],
                "acEmail": member_data["acEmail"],
                "acPhoneNo": member_data["acPhoneNo"],
                "msType": member_data["msType"],
                "msFName": member_data["msFName"],
                "msLName": member_data["msLName"],
                "msEmail": member_data["msEmail"],
                "msPhoneNo": member_data["msPhoneNo"],
                "msDOB": member_data["msDOB"],
                "msAnniversary ": member_data["msAnniversary"],
                "founderName1 ": member_data["founderName1"],
                "founderName2 ": member_data["founderName2"],
                "founderNote ": member_data["founderNote"],
                "fDrink ": member_data["fDrink"],
                "fFilm ": member_data["fFilm"],
                "fitnessActivity ": member_data["fitnessActivity"],
                "fHerb ": member_data["fHerb"],
                "hobby": member_data["hobby"],
                "haveChildren" : member_data["haveChildren"],
                "totalChildren": member_data["totalChildren"],
                "childrens": member_data["childrens"],
                "isActive": member_data["isActive"]
            }
            resp = message(True, "Member Data Found")
            resp["data"] = final_data
            return resp, 200
        
        return err_resp(
            "Member User Not Found",
            "member_404",
            404
        )
    
    @staticmethod
    def post_member_data(data):
        try:
            final_data = {
                "imageUrl": data.get("imageUrl", ""),
                "gender": data.get("gender"),
                "title": data.get("title"),
                "firstName": data.get("firstName"),
                "middleName": data.get("middleName", ""),
                "lastName": data.get("lastName"),
                "dob": data.get("dob"),
                "email": data.get("email"),
                "phoneNo": data.get("phoneNo"),
                "address": data.get("address"),
                "jobTitle": data.get("jobTitle"),
                "company": data.get("company", ""),
                "industry": data.get("industry", ""),
                "mNo": data.get("mNo"),
                "mType":data.get("mType"),
                "startDate": data.get("startDate"),
                "endDate": data.get("endDate"),
                "acType": data.get("acType"),
                "acFName": data.get("acFName",""),
                "acLName": data.get("acLName",""),
                "acEmail": data.get("acEmail",""),
                "acPhoneNo": data.get("acPhoneNo",""),
                "msType": data.get("msType"),
                "msFName": data.get("msFName",""),
                "msLName": data.get("msLName",""),
                "msEmail": data.get("msEmail",""),
                "msPhoneNo": data.get("msPhoneNo",""),
                "msDOB": data.get("msDOB",""),
                "msAnniversary": data.get("msAnniversary",""),
                "founderName1": data.get("founderName1",""),
                "founderName2": data.get("founderName2",""),
                "founderNote": data.get("founderNote",""),
                "fDrink": data.get("fDrink",""),
                "fFilm": data.get("fFilm",""),
                "fitnessActivity": data.get("fitnessActivity",""),
                "fHerb": data.get("fHerb",""),
                "hobby": data.get("hobby", []),
                "haveChildren" : data.get("haveChildren", False),
                "totalChildren": data.get("totalChildren", 0),
                "childrens": data.get("childrens", []),
                "isActive": data.get("isActive", True)
            }
            member_data = app.db.members.find_one({"$or":[{"phoneNo": final_data["phoneNo"]},{"mNo": final_data["mNo"]}]}, {"_id": 0})
            if member_data:
                if member_data["mNo"] == final_data["mNo"]:
                    return err_resp(
                        "Member Number Is Already Taken.",
                        "member_409",
                        409
                    )
                else:
                    return err_resp(
                        "Mobile Number Is Already Used.",
                        "member_409",
                        409
                    )
            app.db.members.insert_one(final_data)
            resp = message(True, "Member Data Inserted")
            resp["data"] = []
            return resp, 201
        
        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def patch_member_data(data):
        id = data.get("id")
        if not validate.validateMongoId(id):
            resp = message(True, "Missing/Incorrect Object Id")
            return resp, 422
        member_data = app.db.members.find_one({"_id": ObjectId(id)}, {"_id": 0, "phoneNo": 0})
        if member_data:
            member_data.update((k, data[k]) for k in (member_data.keys() & data.keys()))
            app.db.members.update_one({"_id": ObjectId(id)},{"$set": member_data})
            resp = message(True, "Member Data Updated")
            resp["data"] = []
            return resp, 200

        return err_resp(
            "Member User Not Found",
            "member_404",
            404
        )

    @staticmethod
    def delete_member_data(id):
        try:
            if not validate.validateMongoId(id):
                resp = message(True, "Missing/Incorrect Object Id")
                return resp, 422
            member_data = app.db.members.find_one({"_id": ObjectId(id)})
            if member_data:
                app.db.members.delete_one({"_id": ObjectId(id)})
                resp = message(True, "Member Data Deleted")
                resp["data"] = []
                return resp, 200

            return err_resp(
                "Member User Not Found",
                "member_404",
                404
            )
        
        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_all_member_data(q, skip, limit):
        try:
            final_data = []
            query = {}
            if len(str(q)) != 0:
                query["$or"] = [
                    {"firstName": {'$regex': str(q), '$options': 'i'}}, 
                    {"lastName": {'$regex': str(q), '$options': 'i'}}, 
                    {"middleName": {'$regex': str(q), '$options': 'i'}}, 
                    {"email": {'$regex': str(q), '$options': 'i'}},
                    {"phoneNo": {'$regex': str(q), '$options': 'i'}},
                    {"mNo": {'$regex': str(q), '$options': 'i'}}
                ]
            query["isActive"] = "True"
            member_data = app.db.members.find(query).skip(skip).limit(limit)
            total_count = app.db.members.count_documents(query)
            if total_count > 0:
                for i in member_data:
                    final_data.append({
                        "id": str(i["_id"]),
                        "imageUrl": i["imageUrl"],
                        "firstName": i["firstName"],
                        "middleName": i["middleName"],
                        "lastName": i["lastName"],
                        "mNo": i["mNo"]
                    })
                resp = message(True, "Member Users Found.")
                resp["data"] = final_data
                resp["total_count"] = total_count
                return resp, 200

            return err_resp(
                "Member User Not Found.",
                "member_404",
                404
            )
        except Exception as error:
            app.logger.error(error)
            return internal_err_resp()


    @staticmethod
    def get_auth_member(data):
        
        if str(data["userType"]) == 'member':
            member_data = app.db.members.find_one({"$or":[{'phoneNo': data.get("data")},{'email':data.get("data")}]})
            if not member_data:
                return err_resp(
                    "member user not found",
                    "user not found",
                    404
                )
        
        else:
            return err_resp(
                    "Please Check UserType",
                    "Invalid UserType",
                    400
                )

        otp = randint(100000, 999999)
        sms_msg = """Your One Time Password is : {} , Please Keep This Code Private"""

        if data.get("mode") == "phone":
            res = sms.send_sms(data.get("data"), sms_msg.format(str(otp)))

        if data.get("mode") == "email":
            res = email.send_email(data.get("data"), sms_msg.format(str(otp)))

        if res['status']:
            otpData={
                    'otp':otp,
                    'createdAt':int(time.time()),
                    'expireAt' : int(time.time()) + 6000,
                    # 'userId':str(admin_data['_id']),
                    'verified':False,
                    'attempt':1
                }

            if str(data["userType"]) == 'member':
                otpData["userId"] = str(member_data['_id'])

            app.db.verificationCode.delete_one({"userId": otpData["userId"]})
            app.db.verificationCode.insert_one(otpData)
            otp_data = app.db.verificationCode.find_one({"userId": otpData["userId"]})
            otpId = otp_data['_id']

            resp={}
            resp['otpId']=str(otpId)
            resp["message"]="OK"
            return resp, 200

        return err_resp(
                    "failed to send otp try again",
                    "error while sending otp",
                    419
                )

    @staticmethod
    def get_verify_member(data):
        otpData = app.db.verificationCode.find_one({"_id":ObjectId(data.get("otpId"))})
        if not otpData:
            return err_resp(
                    "not valid otpId",
                    "check your otp id",
                    400
                )
        if otpData['expireAt'] < int(time.time()):
            return err_resp(
                    "otp code expire",
                    "check your otp code is expire",
                    400
                )
        if otpData['attempt'] > 3:
            return err_resp(
                    "attempt maximum limit reached",
                    "attempt maximum limit reached",
                    400
                )
        if str(data.get("otpCode")) != str(otpData['otp']):
            count = otpData['attempt'] + 1
            app.db.verificationCode.update_one({"_id":ObjectId(data.get("otpId"))},{'$set':{"attempt":count}})
            return err_resp(
                    "Invalid otp code",
                    "check your otp code",
                    400
                )
        if otpData['verified']==True:
            return err_resp(
                    "already verified otp code",
                    "already verified otp code",
                    400
                )

        final_data = {}

        if str(data["userType"]) == 'member':
            member_data = app.db.members.find_one({"_id":ObjectId(otpData['userId'])})

            if member_data:
                final_data = {
                    "user_id": str(member_data["_id"]),
                    "isActive": member_data["isActive"],
                    "email" : member_data["email"],
                    "imageUrl": member_data["imageUrl"],
                    "gender": member_data["gender"],
                    "title": member_data["title"],
                    "firstName": member_data["firstName"],
                    "middleName": member_data["middleName"],
                    "lastName": member_data["lastName"],
                    "dob": member_data["dob"],
                    "phoneNo": member_data["phoneNo"],
                    "address": member_data["address"],
                    "company": member_data["company"],
                    "industry": member_data["industry"],
                    "jobTitle": member_data["jobTitle"],
                    "mNo": member_data["mNo"],
                    "mType": member_data["mType"],
                    "startDate": member_data["startDate"],
                    "endDate": member_data["endDate"],
                    "acType": member_data["acType"],
                    "acFName": member_data["acFName"],
                    "acLName": member_data["acLName"],
                    "acEmail": member_data["acEmail"],
                    "acPhoneNo": member_data["acPhoneNo"],
                    "msType": member_data["msType"],
                    "msFName": member_data["msFName"],
                    "msLName": member_data["msLName"],
                    "msEmail": member_data["msEmail"],
                    "msPhoneNo": member_data["msPhoneNo"],
                    "msDOB": member_data["msDOB"],
                    "msAnniversary" : member_data["msAnniversary"],
                    "founderName1" : member_data["founderName1"],
                    "founderName2" : member_data["founderName2"],
                    "founderNote" : member_data["founderNote"],
                    "fDrink" : member_data["fDrink"],
                    "fFilm" : member_data["fFilm"],
                    "fitnessActivity" : member_data["fitnessActivity"],
                    "fHerb" : member_data["fHerb"],
                    "hobby" : member_data["hobby"],
                    "haveChildren" :member_data["haveChildren"],
                    "totalChildren" : member_data["totalChildren"],
                    "childrens" : member_data["childrens"]
                }
                app.db.verificationCode.update_one({"_id":ObjectId(data.get("otpId"))},{'$set':{"verified":True}})
                resp = {}
                resp["data"] = final_data
                resp["tokens"] = auth.encodeAccessToken(otpData['userId'],"member",member_data["mType"],{})
                return resp, 200
            else:
                return err_resp(
                    "Member User Not Found",
                    "member_404",
                    404
                )

        else:
            return err_resp(
                    "Please Check UserType",
                    "Invalid UserType",
                    400
                )

