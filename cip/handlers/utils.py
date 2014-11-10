from cip.handler import BaseHandler


class ReturningHandler(BaseHandler):
    """
    A returning handler that always terminates the pipeline.
    You configure the response string, code and http headers.

    config:
        data: '' (default)
        code: 200 (default)
        headers: {} (default)

    supports all request types
    """

    def __init__(self, **kwargs):
        super(ReturningHandler, self).__init__(**kwargs)
        self.data = self.config.get('data', '')
        self.code = self.config.get('code', 200)
        self.headers = self.config.get('headers', {})

    def __call__(self, request, path=None, next_handler=None):
        return self.data, self.code, self.headers
