from marshmallow import Schema, fields

class ReservationSchema(Schema):
    member = fields.Str(required=True)
    memberId = fields.Str(required=True)
    category = fields.Str(required=True)
    categoryId = fields.Str(required=True)
    guests = fields.Int(default=0, required=True)
    date = fields.Str(required=True)
    startTime = fields.Str(required=True)
    endTime = fields.Str(required=True)
    areaId = fields.Int(required=True)
    area = fields.Str(required=True)
    

