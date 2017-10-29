class MailServiceError(Exception):
    """Generic internal exception for mail service
    """
    def __init__(self, *args, service):
        super().__init__(*args)
        self.service = service


class SendingFailed(MailServiceError):
    """Exception indicating that email was not sent (e.g. connection problems)
    Request can be repeated
    """
    def __init__(self, *args, reason, **kwargs):
        super().__init__(*args, **kwargs)
        self.reason = reason


class ClientError(SendingFailed):
    """Indicates that there is some misconfiguration on client side and
    usually means that service will need fixing (e.g authorization error will need regeneration of token).
    Repeating request has no chance of success
    """


class UnrecognizedResponse(MailServiceError):
    """Indicates that non standard response was returned and it's not known if email was sent
    Requests should not be repeated
    """
    def __init__(self, *args, status_code, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_code = status_code
