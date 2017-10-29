import urllib.error

import flask

import sendgrid
from sendgrid.helpers import mail
from werkzeug import local

from common import utils

from smacc_email import error

SERVICE_NAME = 'sendgrid'
SENDGRID_API_KEY_FIELD_NAME = 'SENDGRID_API_KEY'


def send_email(*, from_email: str, to_email: str, subject: str, content: str):
    try:
        response = _send_email_sendgrid(from_email=from_email, to_email=to_email,
                                        subject=subject, content=content)
    except urllib.error.URLError:
        raise error.SendingFailed(reason='Connection')
    else:
        if response.status == 202:
            return
        elif response.status == 401:
            raise error.ClientError(reason='Authorization')
        elif response.status == 413:
            raise error.ClientError(reason='Content too Large')
        elif response.status == 400:
            raise error.ClientError(reason='Bad request')
        else:
            raise error.UnrecognizedResponse(status_code=response.status)


def _send_email_sendgrid(*, from_email: str, to_email: str, subject: str, content: str):
    mail_request = mail.Mail(
        from_email=sendgrid.Email(from_email),
        to_email=sendgrid.Email(to_email),
        subject=subject,
        content=mail.Content("text/plain", content),
    )
    return _sendgrid_client.mail.send.post(request_body=mail_request.get())


def configure_sendgrid(environment: dict):
    return {
        SENDGRID_API_KEY_FIELD_NAME: environment[SENDGRID_API_KEY_FIELD_NAME],
    }


@local.LocalProxy
@utils.flask_global_cached_object
def _sendgrid_client():
    return sendgrid.SendGridAPIClient(apikey=flask.current_app.config[SENDGRID_API_KEY_FIELD_NAME]).client
