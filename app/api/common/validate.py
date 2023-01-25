import bson

def validateMongoId(id):
    return bson.objectid.ObjectId.is_valid(id)
