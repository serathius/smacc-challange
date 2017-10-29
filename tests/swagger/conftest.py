import pytest
from bravado.client import SwaggerClient

from common.test_client import FlaskHttpClient

import smacc_email.app
from smacc_email import settings


@pytest.yield_fixture(scope='function', autouse=True)
def app(api_environment):
    app = smacc_email.app.create_app(settings.api_config(api_environment))
    yield app


@pytest.fixture(scope='function')
def swagger_client(client, swagger_client_config):
    return SwaggerClient.from_url(
        '/api/v1/email/swagger.json',
        http_client=FlaskHttpClient(client),
        config=swagger_client_config,
    )


@pytest.fixture
def swagger_client_config():
    return {
        'validate_requests': True,
        'validate_responses': True,
        'validate_swagger_spec': True,
        'also_return_response': True,
    }


@pytest.fixture
def api_environment():
    return {}
