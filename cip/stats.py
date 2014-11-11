import statsd
import time


class NullStatsdClient(object):
    """
    Minimalistic Null/Mock Statsd Client so that we can always call any stats_client method and
    it will fail silently if not configured.

    We are not yet implementing pipelines/timers as not used at the moment.
    """
    def timing(self, *args, **kwargs):
        pass

    def incr(self, *args, **kwargs):
        pass

    def decr(self, *args, **kwargs):
        pass

    def gauge(self, *args, **kwargs):
        pass

    def set(self, *args, **kwargs):
        pass


def setup_stats_client(app):
    """
    initializes statsd client for the app based on app.config
    app.stats_client = statsd.StatsClient()
    """
    statsd_config = app.config.get('statsd', {})
    if statsd_config.get('enabled', False):
        host = statsd_config.get('host', '127.0.0.1')
        port = statsd_config.get('host', 8125)
        prefix = statsd_config.get('prefix', 8125)
        client = statsd.StatsClient(host=host, port=port, prefix=prefix)
        app.stats_client = client
    else:
        app.logger.warn("statsd is not configured")
        app.stats_client = NullStatsdClient()
    return app


def get_duration_ms(start_time):
    """
    :param start_time: start time float as returned by time.time()
    :return: returns delta time in ms between start_time and current time
    """
    end_time = time.time()
    return int((end_time - start_time) * 1000)

