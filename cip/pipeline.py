from logging import getLogger
import uuid
import traceback
import json

from flask import request
from flask import current_app

from cip.handler import get_handler
from cip.handler import HandlerNotImplementedException


class PipelineException(Exception):
    pass


DEFAULT_METHODS = [
    'head',
    'post',
    'get'
]


class Pipeline(object):
    def __init__(self, pipeline_config, logger=getLogger(__name__)):
        self.handlers = []
        self.log = logger
        self.methods = pipeline_config.get('methods', DEFAULT_METHODS)
        for handler_config in pipeline_config['handlers']:
            handler_config['logger'] = self.log
            handler = get_handler(handler_config['handler'], **handler_config)
            self.handlers.append(handler)

    def __call__(self, path=None):
        req_uuid = str(uuid.uuid4())
        for handler in self.handlers:
            self.log.debug("[{}] Executing handler:{} with path:{}".format(
                req_uuid, handler.__class__, path))

            env = current_app.config.get('environment', 'production')
            try:
                # We return on the first handler that returns
                response = handler(request, path=path)
                if response:
                    return response
            except HandlerNotImplementedException:
                if env == 'production':
                    return (req_uuid, 404, {})
                else:
                    return (traceback.format_exc(), 404, {})
            except Exception, e:
                msg = {
                    'request_id': req_uuid,
                    'handler_class': str(handler.__class__),
                    'message': traceback.format_exc(),
                    'headers': str(request.headers),
                    'request_data': str(request.data)
                }
                self.log.error(json.dumps(msg))

                if env == 'production':
                    return (req_uuid, 500, {})
                else:
                    return (traceback.format_exc(), 500, {})

