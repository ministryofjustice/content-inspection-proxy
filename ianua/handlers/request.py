import requests
from requests.packages.urllib3.response import HTTPResponse
from urlparse import urlsplit



from ianua.handler import BaseHandler


class RequestHandler(BaseHandler):

    EXCLUDE_HEADERS = [
        # Certain response headers should NOT be just tunneled through.
        # For more info, see:
        # http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.5.1
        'Connection', 'Keep-Alive', 'Proxy-Authenticate',
        'Proxy-Authorization', 'TE', 'Trailers', 'Transfer-Encoding',
        'Upgrade',

        # Although content-encoding is not listed among the hop-by-hop headers,
        # it can cause trouble as well.  Just let the server set the value as
        # it should be.
        'Content-Encoding',

        # Since the remote server may or may not have sent the content in the
        # same encoding as we will, let framework worry about what the length
        # should be.
        'Content-Length',

        # Purpose of this proxy is to stay on top of any service so yes we
        # have to overwrite virtual host settings
        'Host',
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
            new_headers.pop(header, None)
        return new_headers

    def url(self, path=None):
        baseurl = self.config['url']

        if path:
            if baseurl.endswith('/'):
                return "{}{}".format(baseurl, path)
            else:
                return "{}/{}".format(baseurl, path)
        else:
            return baseurl

    def get(self, request, path=None):
        url = self.url(path)
        self.log.debug("Requesting GET {}".format(url))

        headers = self.sanitize_headers(request.headers)
        response = requests.get(url, headers=headers)
        return response.content

    def post(self, request, path=None):
        url = self.url(path)
        self.log.debug("Requesting POST {}".format(url))

        headers = self.sanitize_headers(request.headers)
        response = requests.post(url, headers=headers)
        return response.content


class RequestHandlerMock(RequestHandler):

    def get(self, request, path=None):
        url = self.url(path)
        self.log.debug("Mocking GET {}".format(url))

        response = HTTPResponse()
        response.content = "requested:{}".format(urlsplit(url).path)
        return response.content

    def post(self, request, path=None):
        url = self.url(path)
        self.log.debug("Mocking POST {}".format(url))

        response = HTTPResponse()
        response.content = "requested:{}".format(urlsplit(url).path)
        return response.content
