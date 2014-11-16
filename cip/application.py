import json
from logging import FileHandler

from flask import Flask
import logstash

from cip.config import open_config
from cip.pipeline import Pipeline
from cip.stats import setup_stats_client


def setup_routes(app):
    """
    Initializes pipelines and stores them as views in flask/werkzeug router

    :param app: flask application object
    :return: app
    """

    pipelines = {}
    for name in app.config.get('pipelines').keys():
        pipelines[name] = Pipeline(app.config['pipelines'][name], pipeline_name=name, logger=app.logger)

    index = 0
    for route, route_config in app.config.get('routes').iteritems():
        #TODO: get view function as callable object or class
        # I guess we should initialize the object on start and we can make
        # it a singleton
        #
        # flask view classes - are they singletons? or should we have an
        # independent storage
        pipeline_name = route_config.get('pipeline', 'default')
        route_specs = []

        if route.endswith('/'):
            route_specs.append("{}".format(route))
            route_specs.append("{}<path:path>".format(route))
        else:
            route_specs.append("{}".format(route))
            route_specs.append("{}/".format(route))
            route_specs.append("{}/<path:path>".format(route))

        for route_spec in route_specs:
            app.add_url_rule(route_spec, "view{}".format(index),
                             pipelines[pipeline_name],
                             strict_slashes=False,
                             methods=pipelines[pipeline_name].methods)

        app.logger.debug("Added route: {}".format(route))
        index += 1
        # Place dummy handler
    return app


def app_maker(config_file="../config/config.yaml"):
    app = Flask(__name__)
    print("Opening config: {}".format(config_file))

    open_config(app, config_file=config_file)
    setup_stats_client(app)

    if 'log_file' in app.config:
        file_handler = FileHandler(app.config['log_file'])
        file_handler.setFormatter(logstash.LogstashFormatterVersion1)
        app.logger.addHandler(file_handler)

    logstash_config = app.config.get('logstash', {})
    if logstash_config.get('enabled', False):
        host = logstash_config.get('host', '127.0.0.1')
        port = logstash_config.get('port', 5959)
        version = logstash_config.get('version', 1)
        app.logger.addHandler(logstash.LogstashHandler(host, port, version=version))

    setup_routes(app)
    return app
