"""
An example handler that introduces constant delay on your link.
Use is as an example to write your own handler with more advanced de3lay strategies.

example config:
    delay_request: 1.0 (default seconds)
    delay_response: 1.0 (default seconds)

"""
import time
from cip.handler import BaseHandler


class LatencyHandler(BaseHandler):
    def __init__(self, **kwargs):
        super(LatencyHandler, self).__init__(**kwargs)
        self.delay_request = self.config.get('delay_request', 1)
        self.delay_response = self.config.get('delay_response', 1)

    def __call__(self, request, path=None, next_handler=None):
        time.sleep(self.delay_request)
        response = next_handler()
        time.sleep(self.delay_response)
        return response
