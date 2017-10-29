import logging
import urllib.error

import botocore.exceptions
import flask

import sendgrid
from sendgrid.helpers import mail
from werkzeug import local
import boto3

from common import utils

from smacc_email import error

logger = logging.getLogger(__name__)
SENDGRID_API_KEY_FIELD_NAME = 'SENDGRID_API_KEY'
SES_REGION_FIELD_NAME = 'SES_REGION'
SES_ACCESS_KEY_ID_FIELD_NAME = 'SES_ACCESS_KEY_ID'
SES_SECRET_ACCESS_KEY_FIELD_NAME = 'SES_SECRET_ACCESS_KEY'


def send_email(*, from_email: str, to_email: str, subject: str, content: str):
    err = None

    for send_email in [send_email_sendgrid, send_email_ses]:
        try:
            return send_email(from_email=from_email, to_email=to_email, subject=subject, content=content)
        except error.ClientError as e:
            logger.error('Bad usage of service api', extra=dict(
                reason=e.reason,
                service=e.service,
            ))
            err = e
        except error.SendingFailed as e:
            logger.warning('Sending email failed', extra=dict(
                reason=e.reason,
                service=e.service,
            ))
            err = e
        except error.UnrecognizedResponse as e:
            logger.error('Unrecognized response', extra=dict(
                status_code=e.status_code,
                service=e.service,
            ))
            raise
    # What response should be returned if some services have connection problem, other configuration
    # Simplified cause time restrictions to return last exception
    assert err is not None
    raise err


def send_email_sendgrid(*, from_email: str, to_email: str, subject: str, content: str):
    service = 'sendgrid'
    try:
        response = _send_email_sendgrid(from_email=from_email, to_email=to_email,
                                        subject=subject, content=content)
    except urllib.error.URLError:
        raise error.SendingFailed(reason='Connection', service=service)
    else:
        if response.status == 202:
            return
        elif response.status == 401:
            raise error.ClientError(reason='Authorization', service=service)
        elif response.status == 413:
            raise error.ClientError(reason='Content too Large', service=service)
        elif response.status == 400:
            raise error.ClientError(reason='Bad request', service=service)
        else:
            raise error.UnrecognizedResponse(status_code=response.status, service=service)


def send_email_ses(*, from_email: str, to_email: str, subject: str, content: str):
    service = 'ses'
    try:
        response = _send_email_ses(from_email=from_email, to_email=to_email,
                                   subject=subject, content=content)
    except botocore.exceptions.EndpointConnectionError:
        raise error.SendingFailed(reason='Connection', service=service)
    else:
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code == 200:
            return
        else:
            # didn't find information in documentation
            # no time to verify manually
            raise error.UnrecognizedResponse(status_code=status_code, service=service)


def configure_sendgrid(environment: dict):
    return {
        SENDGRID_API_KEY_FIELD_NAME: environment[SENDGRID_API_KEY_FIELD_NAME],
        SES_REGION_FIELD_NAME: environment[SES_REGION_FIELD_NAME],
        SES_ACCESS_KEY_ID_FIELD_NAME: environment[SES_ACCESS_KEY_ID_FIELD_NAME],
        SES_SECRET_ACCESS_KEY_FIELD_NAME: environment[SES_SECRET_ACCESS_KEY_FIELD_NAME],
    }


def _send_email_sendgrid(*, from_email: str, to_email: str, subject: str, content: str):
    mail_request = mail.Mail(
        from_email=sendgrid.Email(from_email),
        to_email=sendgrid.Email(to_email),
        subject=subject,
        content=mail.Content("text/plain", content),
    )
    return _sendgrid_client.mail.send.post(request_body=mail_request.get())


def _send_email_ses(*, from_email: str, to_email: str, subject: str, content: str):
    return _ses_client.send_email(
        Source=from_email,
        Destination={
            'ToAddresses': [to_email],
        },
        Message={
            'Subject': {
                'Data': subject,
                'Charset': 'UTF-8',
            },
            'Body': {
                'Text': {
                    'Data': content,
                    'Charset': 'UTF-8',
                }
            }
        }
    )


@local.LocalProxy
@utils.flask_global_cached_object
def _sendgrid_client():
    return sendgrid.SendGridAPIClient(apikey=flask.current_app.config[SENDGRID_API_KEY_FIELD_NAME]).client


@local.LocalProxy
@utils.flask_global_cached_object
def _ses_client():
    return boto3.client(
        service_name='ses',
        region_name=flask.current_app.config[SES_REGION_FIELD_NAME],
        aws_access_key_id=flask.current_app.config[SES_ACCESS_KEY_ID_FIELD_NAME],
        aws_secret_access_key=flask.current_app.config[SES_SECRET_ACCESS_KEY_FIELD_NAME],
    )
