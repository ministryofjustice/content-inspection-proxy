from logging import getLogger
import uuid
import traceback
import json
import time

from flask import request, make_response
from flask import current_app

from cip.handler import get_handler
from cip.handler import HandlerNotImplementedException
from cip import common


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
            handler.handler_name = handler_config['handler'].split('.')[-1]
            self.handlers.append(handler)

    def __call__(self, path=None):
        req_uuid = request.headers.get('x-request_id', str(uuid.uuid4()))
        req_start_dt = time.time()
        req_stat_name = 'request'
        for handler in self.handlers:
            handler_start_dt = time.time()
            self.log.debug(json.dumps(
                "[{}] Executing handler:{} with path:{}".format(
                    req_uuid, handler.__class__, path)))

            env = current_app.config.get('environment', 'production')
            try:
                # We return on the first handler that returns
                response = handler(request, path=path)
            except HandlerNotImplementedException:
                common.post_stat('unknown_handler', '+1', 'g')
                common.post_stat('error', '+1', 'g')
                if env == 'production':
                    return (req_uuid, 404, {})
                else:
                    return (traceback.format_exc(), 404, {})
            except Exception:
                common.post_stat('error', '+1', 'g')
                msg = {
                    'request_id': req_uuid,
                    'handler_class': handler.handler_name,
                    'message': traceback.format_exc(),
                    'headers': str(request.headers),
                    'request_data': str(request.data)
                }
                self.log.error(json.dumps(msg))
                if env == 'production':
                    return (req_uuid, 500, {})
                else:
                    #TODO: Check request content type and respond appropriately
                    return (traceback.format_exc(), 500, {})
            finally:
                end_dt = time.time()
                common.post_stat(handler.handler_name,
                                 end_dt - handler_start_dt, 'ms')
                common.post_stat(req_stat_name,
                                 end_dt - req_start_dt, 'ms')

            if response:
                common.post_stat('success', '+1', 'g')
                common.post_stat(req_stat_name,
                                 time.time() - req_start_dt, 'ms')
                payload, status_code, headers = response
                if status_code != 200:
                    msg = {
                        'request_id': req_uuid,
                        'handler_name': handler.handler_name,
                        'message': str(payload),
                        'headers': str(headers),
                        'request_data': str(request.data),
                        'status_code': str(status_code)
                    }
                    self.log.error(json.dumps(msg))
                payload = req_uuid if env == 'production' else payload
                resp = make_response(payload, status_code)
                resp.headers = dict(headers)
                return resp
        common.post_stat('no_response', '+1', 'g')
        common.post_stat(req_stat_name, time.time() - req_start_dt, 'ms')