"""
Handler to recreate request on target host. Terminates the pipeline.

example_config:
    verify: True (default; can be also a path to CA_BUNDLE; overwritten by ENV variable CURL_CA_BUNDLE)
    url: i.e. http://google.com/ (overwritten by ENV variable CIP_REQ_URL)
    cert: None (default; specific cert or a list; see: http://docs.python-requests.org/en/latest/user/advanced/#ssl-cert-verification)

example_config_with_client_cert:
    verify: False (let's not verify remote cert)
    url: https://foo.bar/baz
    cert:
      - /path/client.crt
      - /path/client.key

"""
import os
import httplib
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
            self.log.debug("updating request to use url: {}".format(self.config['url']))
        self.url = self.config['url']
        self.verify = self.config.get('verify', True)
        self.cert = self.config.get('cert', None)

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

    def base_request_methods(self, request, path=None, method=None, next_handler=None):
        method_dict = {
            'get': requests.get,
            'post': requests.post,
            'head': requests.head
        }

        url = self.geturl(path)
        self.log.debug("Requesting {}: {}".format(
            request.method.upper(), url))
        headers = self.sanitize_headers(request.headers)
        request_method = method_dict[request.method.lower()]
        response = request_method(url, request.data, verify=self.verify, cert=self.cert, headers=headers)
        response.headers = self.sanitize_headers(response.headers)
        return response.text, response.status_code, response.headers.items()

    def geturl(self, path=None):
        """
        merges url and path trying to be smart about backslash
        :param path: path from request
        :return: merged url + path
        """
        baseurl = self.url
        if path:
            if baseurl.endswith('/'):
                return "{}{}".format(baseurl, path)
            else:
                return "{}/{}".format(baseurl, path)
        else:
            return baseurl


class RequestHandlerMock(RequestHandler):
    def get(self, request, path=None, next_handler=None):
        url = self.url(path)
        self.log.debug("Mocking GET {}".format(url))
        return "requested:{}".format(urlsplit(url).path), httplib.OK, {}

    def post(self, request, path=None, next_handler=None):
        url = self.url(path)
        self.log.debug("Mocking POST {}".format(url))
        return "requested:{}".format(urlsplit(url).path), httplib.OK, {}
