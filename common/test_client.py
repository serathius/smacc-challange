import flask
from flask.testing import FlaskClient

import bravado.http_client
import bravado.http_future
import bravado_core.response


class FlaskHttpClient(bravado.http_client.HttpClient):
    def __init__(self, client: FlaskClient):
        self._client = client

    def request(self, request_params, operation=None, response_callbacks=None,
                also_return_response=False):
        test_future = FlaskTestFutureAdapter(request_params, self._client)

        return bravado.http_future.HttpFuture(
            test_future,
            FlaskTestResponseAdapter,
            operation,
            response_callbacks,
            also_return_response)


class FlaskTestFutureAdapter:
    def __init__(self, request_params, client: FlaskClient, response_encoding='utf-8'):
        self._request_params = request_params
        self._response_encoding = response_encoding
        self._client = client

    def result(self, **_):
        path = self._request_params['url'].replace('http://localhost', '')
        return self._client.open(
            path=path,
            query_string=self._request_params.get('params', {}),
            headers=self._request_params.get('headers'),
            data=self._request_params.get('data'),
            method=self._request_params.get('method'))


class FlaskTestResponseAdapter(bravado_core.response.IncomingResponse):
    def __init__(self, response: flask.Response):
        self._response = response

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def text(self):
        return self._response.text

    @property
    def headers(self):
        return self._response.headers

    def json(self, **kwargs):
        return self._response.json
