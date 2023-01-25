from marshmallow import Schema, fields

class Attendees(Schema):
    id = fields.Str()
    name = fields.Str()

class EventSchema(Schema):
    eventTitle = fields.Str(required=True)
    eventNature = fields.Str(required=True)
    eventVenue = fields.Str(required=True)
    eventAbout = fields.Str(required=True)
    eventDate = fields.Str(required=True)
    eventTime = fields.Str(required=True)
    isMembersOnly = fields.Bool(required=True)
    eventImage = fields.Str(required=True)
    attendees=fields.List(fields.Nested(Attendees))
