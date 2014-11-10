"""
A generic throttling handler.

expected config:
    redis_key_prefix: global-rate-limit (default)
    redis_url: None (default)
    limit: 60
    per: 1 (default seconds)
    expiration_window: 0 (default)

Above configuration can be read as:
Let's limit the pipeline to 60 requests per 1s. Where expiration window is 0s as we believe that all clients will have
fully synchronised clocks. On top of it let's connect to local redis and prefix all keys with global-rate-limit.

Make sure to assign different redis_key_prefix for each rate limiting bucket

Based on: http://flask.pocoo.org/snippets/70/
"""
import time

from redis import Redis
from cip.handler import BaseHandler

HTTP_TOO_MANY_REQUESTS = 429

class ThrottlingHandler(BaseHandler):
    def __init__(self, **kwargs):
        super(ThrottlingHandler, self).__init__(**kwargs)
        self.redis_key_prefix = self.config.get('redis_key_prefix', 'global-rate-limit')
        self.redis_url = self.config.get('redis_url', None)
        self.redis = Redis(self.redis_url)
        self.limit = self.config['limit']
        self.per = self.config.get('per', 1)
        self.expiration_window = self.config.get('expiration_window', 0)

    def __call__(self, request, path=None, next_handler=None):
        reset = (int(time.time()) // self.per) * self.per + self.per
        slot_key = "{}-{}".format(self.redis_key_prefix, reset)

        p = self.redis.pipeline()
        p.incr(slot_key)
        p.expireat(slot_key, reset + self.expiration_window)

        slot_value = p.execute()[0]

        # remaining = max(self.limit - slot_value, 0)
        is_over_limit = slot_value > self.limit

        if is_over_limit:
            return "", HTTP_TOO_MANY_REQUESTS, {}

        return next_handler()
