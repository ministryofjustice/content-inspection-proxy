import os
import json
import requests
from urlparse import urlsplit

from cip.handler import BaseHandler, GetHandlerMixin, PostHandlerMixin, HeadHandlerMixin


class RequestHandler(BaseHandler, GetHandlerMixin, PostHandlerMixin, HeadHandlerMixin):

    EXCLUDE_HEADERS = [
        # Certain response headers should NOT be just tunneled through.
        # For more info, see:
        # http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.5.1
        'connection', 'keep-alive', 'proxy-authenticate',
        'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
        'Upgrade',

        # Although content-encoding is not listed among the hop-by-hop headers,
        # it can cause trouble as well.  Just let the server set the value as
        # it should be.
        'content-encoding',

        # Since the remote server may or may not have sent the content in the
        # same encoding as we will, let framework worry about what the length
        # should be.
        'content-length',

        # Purpose of this proxy is to stay on top of any service so yes we
        # have to overwrite virtual host settings
        'host',
    ]

    def __init__(self, **kwargs):
        super(RequestHandler, self).__init__(**kwargs)
        if 'CIP_REQ_URL' in os.environ:
            self.config['url'] = os.environ['CIP_REQ_URL']

    @classmethod
    def sanitize_headers(cls, headers):
        """
        removes headers that shall not be passed through
        :param headers: headers dictionary
        :return: updated headers dictionary
        """
        new_headers = dict(headers)
        for header in cls.EXCLUDE_HEADERS:
            if header.lower() in new_headers:
                new_headers.pop(header, None)
        return new_headers

    def base_method(self, request, path=None, method=None, next_handler=None):
        # let's make sure we haven't been misconfigured
        method_dict = {
            'get': requests.get,
            'post': requests.post,
            'head': requests.head
        }

        url = self.url(path)
        self.log.debug(json.dumps("Requesting {}: {}".format(
            request.method.upper(), url)))
        headers = self.sanitize_headers(request.headers)
        request_method = method_dict[method_dict.keys()]
        response = request_method(url, request.data, headers=headers)
        response.headers = self.sanitize_headers(response.headers)
        return response.text, response.status_code, response.headers.items()


class RequestHandlerMock(RequestHandler):
    def get(self, request, path=None, next_handler=None):
        url = self.url(path)
        self.log.debug(json.dumps("Mocking GET {}".format(url)))
        return "requested:{}".format(urlsplit(url).path), 200, {}

    def post(self, request, path=None, next_handler=None):
        url = self.url(path)
        self.log.debug(json.dumps("Mocking POST {}".format(url)))
        return "requested:{}".format(urlsplit(url).path), 200, {}
