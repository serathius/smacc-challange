from common.sentry import configure_sentry

from smacc_email import mail


def api_config(environment):
    config = {}
    config.update(configure_sentry(environment))
    config.update(mail.configure_sendgrid(environment))
    return config
