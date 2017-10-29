import flask_restful
import marshmallow

from smacc_email import error
from smacc_email import mail
from smacc_email import schemas

manager = flask_restful.Api(prefix='/api/v1/email/')


class EmailResource(flask_restful.Resource):
    schema = schemas.EmailRequestSchema(strict=True)

    def post(self):
        email_request = self._extract_email_request()
        self._send_email(email_request)
        return '', 202

    def _extract_email_request(self):
        data = flask_restful.request.get_json()
        if not data:
            raise flask_restful.abort(400)
        try:
            return self.schema.load(data).data
        except marshmallow.ValidationError:
            raise flask_restful.abort(400)

    def _send_email(self, email_request):
        try:
            return mail.send_email(
                from_email=email_request.from_email,
                to_email=email_request.to_email,
                subject=email_request.subject,
                content=email_request.content,
            )
        except error.ClientError:
            raise flask_restful.abort(502)
        except error.SendingFailed:
            raise flask_restful.abort(503)
        except error.UnrecognizedResponse:
            raise flask_restful.abort(501)


manager.add_resource(EmailResource, '/')
