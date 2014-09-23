import json
import requests
from urlparse import urlsplit

from cip.handler import BaseHandler


class RequestHandler(BaseHandler):

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

    def base_method(self, request, path=None, method=None):
        method_dict = {
            'get': requests.get,
            'post': requests.post,
            'head': requests.head
        }

        if not method or method not in method_dict:
            raise Exception('Invalid method')

        url = self.url(path)
        self.log.debug(json.dumps("Requesting {}: {}".format(
            self.req_method.upper(), url)))
        headers = self.sanitize_headers(request.headers)
        response = method_dict[self.req_method](url, request.data,
                                                headers=headers)
        response.headers = self.sanitize_headers(response.headers)
        return (response.text, response.status_code, response.headers.items())


class RequestHandlerMock(RequestHandler):
    def get(self, request, path=None):
        url = self.url(path)
        self.log.debug(json.dumps("Mocking GET {}".format(url)))
        return "requested:{}".format(urlsplit(url).path)

    def post(self, request, path=None):
        url = self.url(path)
        self.log.debug(json.dumps("Mocking POST {}".format(url)))
        return "requested:{}".format(urlsplit(url).path)
