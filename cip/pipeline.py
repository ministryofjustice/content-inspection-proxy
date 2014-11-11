from logging import getLogger
import functools
import uuid
import traceback
import json
import time
import copy

from flask import request
from flask import current_app

from cip.handler import get_handler
from cip.handler import HandlerNotImplementedException
from cip import common
from cip.stats import get_duration_ms

DEFAULT_METHODS = [
    'get'
]


class PipelineException(Exception):
    pass


class Pipeline(object):
    def __init__(self, pipeline_config, pipeline_name=None, logger=getLogger(__name__)):
        self.handlers = []
        self.log = logger
        self.methods = pipeline_config.get('methods', DEFAULT_METHODS)
        self.pipeline_name = pipeline_name

        for config in pipeline_config['handlers']:
            # deep-copy config so that handlers can't poison it for handlers in different pipelines
            handler_config = copy.deepcopy(config)
            handler_config['logger'] = self.log
            handler_config['handler_name'] = handler_config['handler'].split('.')[-1]
            handler = get_handler(handler_config['handler'], **handler_config)
            self.handlers.append(handler)

    def __call__(self, path=None):
        req_uuid = request.headers.get('x-request_id', str(uuid.uuid4()))
        req_start_dt = time.time()
        req_stat_name = 'request'

        if 'Content-Type' in request.headers \
                and 'xml' in request.headers['Content-Type']:
            out = common.xml_error
            resp_headers = {'Content-Type': 'application/xml'}
        else:
            out = '{}'
            resp_headers = {}

        # creates chain of handlers h0(h1(h2))
        def null_handler():
            pass
        chained_handler = null_handler
        for handler in reversed(self.handlers):
            chained_handler = functools.partial(handler, next_handler=chained_handler, request=request, path=path)

        try:
            response = chained_handler()
        except HandlerNotImplementedException:
            current_app.stats_client.incr('unknown_handler', 1)
            current_app.stats_client.incr('error', 1)
            if not current_app.debug:
                return out.format(req_uuid), 404, resp_headers
            else:
                return out.format(traceback.format_exc()), 404, resp_headers
        except Exception:

            current_app.stats_client.incr('error', 1)
            msg = {
                'request_id': req_uuid,
                'message': traceback.format_exc(),
                'headers': str(request.headers),
                'request_data': str(request.data)
            }
            self.log.error(json.dumps(msg))
            if not current_app.debug:
                return out.format(req_uuid), 500, resp_headers
            else:
                return out.format(traceback.format_exc()), 500, resp_headers
        finally:
            current_app.stats_client.timing(req_stat_name, get_duration_ms(req_start_dt))

        if response:
            current_app.stats_client.incr('success', 1)
            payload, status_code, headers = response
            if 300 > status_code < 200:
                msg = {
                    'request_id': req_uuid,
                    'message': str(payload),
                    'headers': str(headers),
                    'request_data': str(request.data),
                    'status_code': str(status_code)
                }
                self.log.error(json.dumps(msg))
                payload = out.format(req_uuid) if not current_app.debug else payload
            return payload, status_code, dict(headers)

        current_app.stats_client.incr('no_response', 1)
        current_app.stats_client.timing(req_stat_name, get_duration_ms(req_start_dt))
        msg = {
            'request_id': req_uuid,
            'message': 'No response from handlers',
            'headers': str(request.headers),
            'request_data': str(request.data)
        }
        self.log.error(json.dumps(msg))

        if not current_app.debug:
            return out.format(req_uuid), 500, resp_headers
        else:
            return out.format('No response from handlers'), 500, resp_headers
