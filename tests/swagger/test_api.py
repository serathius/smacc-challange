from unittest import mock

import bravado.exception
import pytest

from smacc_email import error


@mock.patch('smacc_email.mail._send_email_sendgrid')
def test_send_email(send_email_sendgrid, swagger_client):
    send_email_sendgrid.return_value = mock.Mock(status=202)
    _, response = swagger_client.email.send_email(email_data={
        'from_email': 'a@a.pl',
        'to_email': 'b@b.pl',
        'content': 'content',
        'subject': 'subject',
    }).result()
    assert response.status_code == 202
    assert send_email_sendgrid.mock_calls == [
        mock.call(from_email='a@a.pl', to_email='b@b.pl', content='content', subject='subject'),
    ]


def test_send_email_bad_from_email(swagger_client):
    with pytest.raises(bravado.exception.HTTPBadRequest):
        swagger_client.email.send_email(email_data={
            'from_email': 'a',
            'to_email': 'b@b.pl',
            'content': 'content',
            'subject': 'subject',
        }).result()


def test_send_email_bad_to_email(swagger_client):
    with pytest.raises(bravado.exception.HTTPBadRequest):
        swagger_client.email.send_email(email_data={
            'from_email': 'a@a.pl',
            'to_email': 'b',
            'content': 'content',
            'subject': 'subject',
        }).result()


def test_send_email_bad_missing_field(swagger_client):
    with pytest.raises(bravado.exception.HTTPBadRequest):
        swagger_client.email.send_email(email_data={
            'from_email': 'a@a.pl',
            'to_email': 'b@b.pl',
            'content': 'content',
        }).result()


@mock.patch('smacc_email.mail._send_email_sendgrid')
def test_send_email_returns_uknown_response(send_email_sendgrid, swagger_client):
    send_email_sendgrid.return_value = mock.Mock(status=201)
    with pytest.raises(bravado.exception.HTTPNotImplemented):
        swagger_client.email.send_email(email_data={
            'from_email': 'a@a.pl',
            'to_email': 'b@b.pl',
            'content': 'content',
            'subject': 'subject',
        }).result()


@mock.patch('smacc_email.mail._send_email_sendgrid')
def test_send_email_returns_internal_server_error(send_email_sendgrid, swagger_client):
    send_email_sendgrid.side_effect = error.SendingFailed(service='sendgrid', reason='Connection')
    with pytest.raises(bravado.exception.HTTPServiceUnavailable):
        swagger_client.email.send_email(email_data={
            'from_email': 'a@a.pl',
            'to_email': 'b@b.pl',
            'content': 'content',
            'subject': 'subject',
        }).result()


@mock.patch('smacc_email.mail._send_email_sendgrid')
def test_send_email_returns_unauthorized(send_email_sendgrid, swagger_client):
    send_email_sendgrid.return_value = mock.Mock(status=401)
    with pytest.raises(bravado.exception.HTTPBadGateway):
        swagger_client.email.send_email(email_data={
            'from_email': 'a@a.pl',
            'to_email': 'b@b.pl',
            'content': 'content',
            'subject': 'subject',
        }).result()


@mock.patch('smacc_email.mail._send_email_sendgrid')
def test_send_email_returns_entity_too_large(send_email_sendgrid, swagger_client):
    send_email_sendgrid.return_value = mock.Mock(status=413)
    with pytest.raises(bravado.exception.HTTPBadGateway):
        swagger_client.email.send_email(email_data={
            'from_email': 'a@a.pl',
            'to_email': 'b@b.pl',
            'content': 'content',
            'subject': 'subject',
        }).result()


@mock.patch('smacc_email.mail._send_email_sendgrid')
def test_send_email_returns_bad_request(send_email_sendgrid, swagger_client):
    send_email_sendgrid.return_value = mock.Mock(status=400)
    with pytest.raises(bravado.exception.HTTPBadGateway):
        swagger_client.email.send_email(email_data={
            'from_email': 'a@a.pl',
            'to_email': 'b@b.pl',
            'content': 'content',
            'subject': 'subject',
        }).result()
