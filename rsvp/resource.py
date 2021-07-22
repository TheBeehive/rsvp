from marshmallow import Schema
from marshmallow.fields import Field, Integer, String


class NumberBool(Field):
    default_error_messages = {"invalid": "Not a valid boolean."}

    def _serialize(self, value, attr, obj, **kwargs):
        return None if value is None else int(value)

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None or value == '':
            return None

        try:
            value = int(value)
        except ValueError as e:
            raise self.make_error("invalid", input=value) from e

        return bool(value)


class RSVPSchema(Schema):
    wedding = NumberBool(data_key='reception')
    vaxxed = NumberBool(missing=None)
    masked = NumberBool(missing=None)

    cocktails = NumberBool(data_key='cocktail')
    cocktails_excess = Integer(data_key='cocktail_excess', missing=None)

    hike = NumberBool()
    phone = String(data_key='mobile', missing=None)

    brunch = NumberBool(missing=None)
