import logging

from common.prometheus import emails_sent_total

from smacc_email import error
from smacc_email.service import sendgrid
from smacc_email.service import ses

logger = logging.getLogger(__name__)


SERVICES = {
    sendgrid.SERVICE_NAME: sendgrid.send_email,
    ses.SERVICE_NAME: ses.send_email,
}


def send_email(*, from_email: str, to_email: str, subject: str, content: str):
    err = None

    for service, send_email in SERVICES.items():
        try:
            send_email(from_email=from_email, to_email=to_email, subject=subject, content=content)
            emails_sent_total.labels(service=service).inc()
            return
        except error.ClientError as e:
            logger.error('Bad usage of service api', extra=dict(
                reason=e.reason,
                service=service,
            ))
            err = e
        except error.SendingFailed as e:
            logger.warning('Sending email failed', extra=dict(
                reason=e.reason,
                service=service,
            ))
            err = e
        except error.UnrecognizedResponse as e:
            logger.error('Unrecognized response', extra=dict(
                status_code=e.status_code,
                service=service,
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
