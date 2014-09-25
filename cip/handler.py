import importlib
import os


class HandlerNotImplementedException(NotImplementedError):
    pass


class BaseHandler(object):

    def __init__(self, **kwargs):
        self.config = kwargs
        self.log = kwargs['logger']

    def __call__(self, request, path=None):
        req_method = request.method.lower()
        method_func = getattr(self, req_method)
        if method_func is None:
            raise HandlerNotImplementedException(req_method)
        self.req_method = req_method
        return method_func(request, path)

    def url(self, path=None):
        if 'CIP_REQ_URL' in os.environ:
            baseurl = os.environ['CIP_REQ_URL']
        else:
            baseurl = self.config['url']
        if path:
            if baseurl.endswith('/'):
                return "{}{}".format(baseurl, path)
            else:
                return "{}/{}".format(baseurl, path)
        else:
            return baseurl

    def get(self, request, path=None):
        return self.base_method(request, path=None, method='get')

    def head(self, request, path=None):
        return self.base_method(request, path=None, method='head')

    def post(self, request, path=None):
        return self.base_method(request, path=None, method='post')

    def base_method(self, request, path=None, method=None):
        raise HandlerNotImplementedException(method)


def get_handler(class_name, **kwargs):
    """
    Provides initiated Handler object

    :param class_name: Handler class name
    :param kwargs: key/value arguments to pass initiate Handler object with
    :return: initiated Handler object
    """
    #pickup the module
    provider_module = importlib.import_module(
        '.'.join(class_name.split('.')[:-1]))

    #pickup the class
    handler_class = getattr(provider_module, class_name.split('.')[-1])
    assert issubclass(handler_class, BaseHandler)

    #initate the object
    return handler_class(**kwargs)
