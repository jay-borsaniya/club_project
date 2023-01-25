from marshmallow import Schema, fields

class GlobalAccess(Schema):
    name = fields.Str(required=True)
    continent = fields.Str(required=True)
    country = fields.Str(required=True)
    location = fields.Str(required=True)
    url = fields.Str(required=True)
    address = fields.Str(required=True)
    facilities = fields.Str(required=True)
    recommendation = fields.Str(required=True)
    benefits = fields.Str(required=True)
    visits = fields.Str(required=True)
    clubLogos=fields.List(fields.Str(required=True))
    clubMaps=fields.List(fields.Str(required=True))
    clubPhotos=fields.List(fields.Str(required=True))
