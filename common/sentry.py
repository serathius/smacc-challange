import logging

from raven.contrib.flask import Sentry


def configure_sentry(environment: dict):
    return {
        'SENTRY_DSN': environment.get('SENTRY_DSN'),
        'SENTRY_TRANSPORT': 'raven.transport.requests.RequestsHTTPTransport',
    }


def register_sentry(app):
    if app.config.get('SENTRY_DSN', False):
        Sentry(app, logging=True, level=logging.WARNING)
