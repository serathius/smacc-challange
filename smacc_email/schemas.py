import typing

import flask_marshmallow
import marshmallow
from marshmallow import fields

manager = flask_marshmallow.Marshmallow()


class EmailRequestSchema(flask_marshmallow.Schema):
    from_email = fields.Email(allow_none=False, required=True)
    to_email = fields.Email(allow_none=False, required=True)
    subject = fields.String(allow_none=False, required=True)
    content = fields.String(allow_none=False, required=True)

    @marshmallow.post_load
    def fill_email_request(self, data):
        return _EmailRequest(**data)


class _EmailRequest(typing.NamedTuple):
    from_email: str
    to_email: str
    subject: str
    content: str
