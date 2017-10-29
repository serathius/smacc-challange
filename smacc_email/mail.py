import logging

from smacc_email import error
from smacc_email.service import sendgrid
from smacc_email.service import ses

logger = logging.getLogger(__name__)
SENDGRID_API_KEY_FIELD_NAME = 'SENDGRID_API_KEY'
SES_REGION_FIELD_NAME = 'SES_REGION'
SES_ACCESS_KEY_ID_FIELD_NAME = 'SES_ACCESS_KEY_ID'
SES_SECRET_ACCESS_KEY_FIELD_NAME = 'SES_SECRET_ACCESS_KEY'


def send_email(*, from_email: str, to_email: str, subject: str, content: str):
    err = None

    for send_email in [sendgrid.send_email, ses.send_email]:
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


def configure_email(environment: dict):
    config = {}
    config.update(sendgrid.configure_sendgrid(environment))
    config.update(ses.configure_ses(environment))
    return config
