import json
import importlib
import time
import uuid

from flask import current_app

from cip.stats import get_duration_ms


class HandlerNotImplementedException(NotImplementedError):
    pass


class BaseHandler(object):
    """
    when inheriting implement methods like get, post,...
    you can use mixins GetHandlerMixin, PostHandlerMixin,...

    make sure you validate config in __init__

    Note that this object is initialized at the application start and persists within pipeline

    """

    def __init__(self, **kwargs):
        self.config = kwargs
        self.log = kwargs['logger']
        self.handler_name = kwargs['handler_name']

    def __call__(self, request, path=None, next_handler=None):
        """
        Based on request.method calls appropriate function
        If request function does not exist than raises HandlerNotImplementedException
        """
        req_uuid = request.headers.get('x-request_id', str(uuid.uuid4()))
        req_start_dt = time.time()
        self.log.debug("[{}] Executing handler:{} with path:{}".format(
                       req_uuid, self.__class__, path))
        req_method = request.method.lower()
        method_func = getattr(self, req_method)
        if method_func is None:
            raise HandlerNotImplementedException(req_method)
        response = method_func(request, path, next_handler=next_handler)
        if response:
            code = response[1]
        else:
            code = None
        self.log.debug("[{}] Response from handler:{} with path:{} code:{}".format(
                       req_uuid, self.__class__, path, code))

        current_app.stats_client.timing(self.handler_name, get_duration_ms(req_start_dt))
        return response

    def url(self, path=None):
        baseurl = self.config['url']
        if path:
            if baseurl.endswith('/'):
                return "{}{}".format(baseurl, path)
            else:
                return "{}/{}".format(baseurl, path)
        else:
            return baseurl


class BaseHandlerMixin(object):
    def base_request_methods(self, request, path=None, method=None, next_handler=None):
        raise HandlerNotImplementedException(method)


class GetHandlerMixin(BaseHandlerMixin):
    def get(self, request, path=None, next_handler=None):
        return self.base_request_methods(request, path=path, method='get', next_handler=next_handler)


class PostHandlerMixin(BaseHandlerMixin):
    def post(self, request, path=None, next_handler=None):
        return self.base_request_methods(request, path=path, method='post', next_handler=next_handler)


class HeadHandlerMixin(BaseHandlerMixin):
    def head(self, request, path=None, next_handler=None):
        return self.base_request_methods(request, path=path, method='head', next_handler=next_handler)


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
