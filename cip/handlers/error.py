from cip.handler import BaseHandler


class ErrorHandler(BaseHandler):
    """
    Handles all requests and returns by default 505 (HTTP Version Not Supported)
    config:
        code: 505 (default)
    """

    def __call__(self, request, path=None, next_handler=None):
        return None, self.config.get('code', 505), {}
