import time

import flask

import prometheus_client
from prometheus_client import exposition

blueprint = flask.Blueprint("prometheus", __name__)

latency_seconds = prometheus_client.Histogram(
    'latency_seconds', 'HTTP Request Latency', ['code', 'method', 'handler']
)
requests_total = prometheus_client.Summary(
    'requests_total', 'HTTP Requests', ['code', 'method', 'handler']
)
emails_sent_total = prometheus_client.Counter(
    'emails_sent_total', 'Emails sent', ['service']
)


@blueprint.before_app_request
def _register_request_start():
    flask.request.prometheus_start_time = time.monotonic()


@blueprint.after_app_request
def _observe_request_end(response):
    request_time = time.monotonic() - flask.request.prometheus_start_time

    latency_seconds.labels(
        code=response.status_code,
        method=flask.request.method,
        handler=flask.request.endpoint,
    ).observe(request_time)
    requests_total.labels(
        code=response.status_code,
        method=flask.request.method,
        handler=flask.request.endpoint,
    ).observe(request_time)
    return response


@blueprint.route("/metrics")
def _metrics():
    payload = exposition.generate_latest()
    return flask.Response(payload, mimetype=exposition.CONTENT_TYPE_LATEST)
