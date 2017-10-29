from common.sentry import configure_sentry


def configure_email(environment: dict):
    return {
    }


def api_config(environment):
    config = {}
    config.update(configure_sentry(environment))
    config.update(configure_email(environment))
    return config
