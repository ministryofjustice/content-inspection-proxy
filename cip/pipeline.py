from logging import getLogger
import random
import uuid
import traceback
import json
import time

from flask import request, make_response
from flask import current_app

from cip.handler import get_handler
from cip.handler import HandlerNotImplementedException
from cip import common


# default is microseconds
def get_duration(req_start_dt, multiplier=1000000):
    end_dt = time.time()
    return int((end_dt - req_start_dt) * multiplier)


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
        # time.sleep(random.randint(0, 5))
        req_stat_name = 'request'
        if 'xml' in request.headers['Content-Type']:
            out = common.xml_error
        else:
            out = '{}'
        for handler in self.handlers:
            self.log.debug(json.dumps(
                "[{}] Executing handler:{} with path:{}".format(
                    req_uuid, handler.__class__, path)))

            env = current_app.config.get('environment', 'production')
            try:
                # We return on the first handler that returns
                response = handler(request, path=path)
            except HandlerNotImplementedException:
                common.post_stat('unknown_handler', '+1', 'c')
                common.post_stat('error', '+1', 'c')
                if env == 'production':
                    return (req_uuid, 404, {})
                else:
                    return (traceback.format_exc(), 404, {})
            except Exception:
                common.post_stat('error', '+1', 'c')
                msg = {
                    'request_id': req_uuid,
                    'handler_class': handler.handler_name,
                    'message': traceback.format_exc(),
                    'headers': str(request.headers),
                    'request_data': str(request.data)
                }
                self.log.error(json.dumps(msg))
                if 'xml' in request.headers['Content-Type']:
                    out = common.xml_error
                else:
                    out = '{}'
                if env == 'production':
                    return (out.format(req_uuid), 500, {})
                else:
                    #TODO: Check request content type and respond appropriately
                    return (out.format(traceback.format_exc()), 500, {})
            finally:
                common.post_stat(handler.handler_name, get_duration(req_start_dt),
                                 'ms')
                common.post_stat(req_stat_name, get_duration(req_start_dt), 'ms')

            if response:
                common.post_stat('success', '+1', 'c')
                common.post_stat(req_stat_name, get_duration(req_start_dt), 'ms')
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

                    payload = out.format(req_uuid)\
                        if env == 'production' else payload
                resp = make_response(payload, status_code)
                resp.headers = dict(headers)
                return resp
        common.post_stat('no_response', '+1', 'c')
        common.post_stat(req_stat_name, get_duration(req_start_dt), 'ms')