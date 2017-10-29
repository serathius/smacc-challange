import flask

import boto3
import botocore.exceptions
from werkzeug import local

from common import utils

from smacc_email import error

SERVICE_NAME = 'ses'
SES_REGION_FIELD_NAME = 'SES_REGION'
SES_ACCESS_KEY_ID_FIELD_NAME = 'SES_ACCESS_KEY_ID'
SES_SECRET_ACCESS_KEY_FIELD_NAME = 'SES_SECRET_ACCESS_KEY'


def send_email(*, from_email: str, to_email: str, subject: str, content: str):
    try:
        response = _send_email_ses(from_email=from_email, to_email=to_email,
                                   subject=subject, content=content)
    except botocore.exceptions.EndpointConnectionError:
        raise error.SendingFailed(reason='Connection')
    else:
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code == 200:
            return
        else:
            # didn't find information in documentation
            # no time to verify manually
            raise error.UnrecognizedResponse(status_code=status_code)


def configure_ses(environment: dict):
    return {
        SES_REGION_FIELD_NAME: environment[SES_REGION_FIELD_NAME],
        SES_ACCESS_KEY_ID_FIELD_NAME: environment[SES_ACCESS_KEY_ID_FIELD_NAME],
        SES_SECRET_ACCESS_KEY_FIELD_NAME: environment[SES_SECRET_ACCESS_KEY_FIELD_NAME],
    }


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
def _ses_client():
    return boto3.client(
        service_name='ses',
        region_name=flask.current_app.config[SES_REGION_FIELD_NAME],
        aws_access_key_id=flask.current_app.config[SES_ACCESS_KEY_ID_FIELD_NAME],
        aws_secret_access_key=flask.current_app.config[SES_SECRET_ACCESS_KEY_FIELD_NAME],
    )
