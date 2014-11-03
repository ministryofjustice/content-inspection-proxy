from logging import getLogger
import functools
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


class PipelineException(Exception):
    pass


class Pipeline(object):
    def __init__(self, pipeline_config, logger=getLogger(__name__)):
        self.handlers = []
        self.log = logger
        for handler_config in pipeline_config['handlers']:
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
        hide_errors = current_app.config.get('hide_errors', True)

        # creates chain of handlers h0(h1(h2()))
        chained_handler = self.handlers[-1]
        for handler in reversed(self.handlers):
            chained_handler = functools.partial(handler, next_handler=chained_handler, request=request, path=path)

        try:
            response = chained_handler()
        except HandlerNotImplementedException:
            common.post_stat('unknown_handler', '+1', 'c')
            common.post_stat('error', '+1', 'c')
            if hide_errors:
                return out.format(req_uuid), 404, resp_headers
            else:
                return out.format(traceback.format_exc()), 404, resp_headers
        except Exception:
            common.post_stat('error', '+1', 'c')
            msg = {
                'request_id': req_uuid,
                'message': traceback.format_exc(),
                'headers': str(request.headers),
                'request_data': str(request.data)
            }
            self.log.error(json.dumps(msg))
            if hide_errors:
                return out.format(req_uuid), 500, resp_headers
            else:
                return out.format(traceback.format_exc()), 500, resp_headers
        finally:
            common.post_stat(req_stat_name,
                             common.get_duration(req_start_dt), 'ms')

        if response:
            common.post_stat('success', '+1', 'c')
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
                payload = out.format(req_uuid) if hide_errors else payload
            # resp = make_response(payload, status_code)
            # resp.headers = dict(headers)
            return payload, status_code, dict(headers)
        common.post_stat('no_response', '+1', 'c')
        common.post_stat(req_stat_name, common.get_duration(req_start_dt), 'ms')
        msg = {
            'request_id': req_uuid,
            'message': 'No response from handlers',
            'headers': str(request.headers),
            'request_data': str(request.data)
        }
        self.log.error(json.dumps(msg))
        if hide_errors:
            return out.format(req_uuid), 500, resp_headers
        else:
            return out.format('No response from handlers'), 500, resp_headers
