from marshmallow import Schema
from marshmallow.fields import Field, Integer, String

__all__ = ("RSVPSchema",)


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
    diet_info = String(missing=None)
    vaxxed = NumberBool(missing=None)
    masked = NumberBool(missing=None)

    cocktails = NumberBool(data_key='cocktail', missing=None)
    cocktails_excess = Integer(data_key='cocktail_excess', missing=None)

    hike = NumberBool(missing=None)
    phone = String(data_key='mobile', missing=None)

    brunch = NumberBool(missing=None)


class IndeterminateRSVPSchema(RSVPSchema):
    plusname = String(missing=None)
    plusvaxxed = NumberBool(missing=None)
    plusmasked = NumberBool(missing=None)
    pluscocktails = NumberBool(data_key='pluscocktail', missing=None)
    plushike = NumberBool(missing=None)
    plusphone = String(data_key='plusmobile', missing=None)
    plusbrunch = NumberBool(missing=None)
