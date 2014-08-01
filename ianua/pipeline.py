#from ianua.singleton import Singleton
from ianua.handler import get_handler
from flask import abort
from flask import request

from logging import getLogger


class PipelineException(Exception):
    pass


DEFAULT_METHODS = [
    'head',
    'post',
    'get'
]

class Pipeline(object):

#    provide_automatic_options = False

    def __init__(self, pipeline_config, logger=getLogger(__name__)):
        self.handlers = []
        self.log = logger
        self.methods = pipeline_config.get('methods', DEFAULT_METHODS)
        for handler_config in pipeline_config['handlers']:
            handler_config['logger'] = self.log
            handler = get_handler(handler_config['handler'], **handler_config)
            self.handlers.append(handler)

    def __call__(self, path=None):
        for handler in self.handlers:
            self.log.debug("Executing handler:{} with path:{}".format(handler.__class__, path))

            response = handler(request, path=path)
            if response:
                return response
        else:
            raise PipelineException("No response available")
