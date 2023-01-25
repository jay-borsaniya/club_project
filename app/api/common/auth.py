from flask import current_app as app
from flask import request
from jose import jwt
import datetime

def token_required(token):
    try:
        resp = {}
        data = jwt.decode(token,app.config['SECRET_KEY'])
        if (data['sub'] == 'admin'):
            resp["msg"] = "Success"
            resp["status"] = 200

        elif (data['sub'] == 'member'):
            resp["msg"] = "Success"
            resp["status"] = 200

        else:
            resp["msg"] = "Access Denied"
            resp["status"] = 403

        
    except Exception as e:
        resp["msg"] = "Unauthorized"
        resp["status"] = 401
    finally:
        return resp

def encodeAccessToken(id, sub, access, meta):
    tokens = {}
    accessToken = jwt.encode({
        "_id":id,
        "sub":sub,
        "access":access,
        "meta": meta,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1500)
    }, app.config["SECRET_KEY"], algorithm="HS256")

    data = {}
    data['access_token'] = accessToken
    return data

