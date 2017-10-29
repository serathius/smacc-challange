import urllib.error
from unittest import mock

import botocore.exceptions
import bravado.exception
import pytest


@mock.patch('smacc_email.service.sendgrid._send_email_sendgrid')
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


@mock.patch('smacc_email.service.ses._send_email_ses')
@mock.patch('smacc_email.service.sendgrid._send_email_sendgrid')
def test_send_email_fails_over_to_ses(send_email_sendgrid, send_email_ses, swagger_client):
    send_email_sendgrid.side_effect = urllib.error.URLError(reason='connection')
    send_email_ses.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
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
    assert send_email_ses.mock_calls == [
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


@mock.patch('smacc_email.service.sendgrid._send_email_sendgrid')
def test_send_email_returns_uknown_response(send_email_sendgrid, swagger_client):
    send_email_sendgrid.return_value = mock.Mock(status=201)
    with pytest.raises(bravado.exception.HTTPNotImplemented):
        swagger_client.email.send_email(email_data={
            'from_email': 'a@a.pl',
            'to_email': 'b@b.pl',
            'content': 'content',
            'subject': 'subject',
        }).result()


@mock.patch('smacc_email.service.ses._send_email_ses')
@mock.patch('smacc_email.service.sendgrid._send_email_sendgrid')
def test_send_email_connection_error(send_email_sendgrid, send_email_ses, swagger_client):
    send_email_sendgrid.side_effect = urllib.error.URLError(reason='connection')
    send_email_ses.side_effect = botocore.exceptions.EndpointConnectionError(endpoint_url='')
    with pytest.raises(bravado.exception.HTTPServiceUnavailable):
        swagger_client.email.send_email(email_data={
            'from_email': 'a@a.pl',
            'to_email': 'b@b.pl',
            'content': 'content',
            'subject': 'subject',
        }).result()
