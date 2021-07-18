from marshmallow import Schema, fields

class RSVPSchema(Schema):
    brunch = fields.Boolean(missing=None)
    wedding = fields.Boolean()
    vaxxed = fields.Boolean(missing=None)
    masked = fields.Boolean(missing=None)
    hike = fields.Boolean()
    phone = fields.Str(missing=None)
    cocktails = fields.Boolean()
    cocktails_excess = fields.Integer(missing=None)

