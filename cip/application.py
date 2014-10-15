import json
from logging import FileHandler
from logging import Formatter
import logging
import os

from flask import Flask

from cip.config import open_config
from cip.pipeline import Pipeline


def blank_view():
    pass


def setup_routes(app):
    """
    Initializes pipelines and stores them as views in flask/werkzeug router

    :param app: flask application object
    :return: app
    """

    pipelines = {}
    for name in app.config.get('pipelines').keys():
        pipelines[name] = Pipeline(app.config['pipelines'][name], app.logger)

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

        app.logger.debug(json.dumps("Added route: {}".format(route)))
        index += 1
        # Place dummy handler
    return app


def app_maker(config_file="../config/config.yaml"):
    app = Flask(__name__)
    @app.route('/dummy', methods=['POST'])
    def dummy():
        return '<success>Bingo</success>'

    if 'CIP_HIDE_ERRORS' in os.environ:
        app.config['hide_errors'] = True

    log_fmt = '{"timestamp":"%(asctime)s", "level": "%(levelname)s",' + \
              '"module": "%(module)s", "location": "%(pathname)s:%(lineno)d]",' + \
              '"payload": %(message)s}'

    if 'log_file' in app.config:
        fh = FileHandler(app.config['log_file'])
        fh.setFormatter(Formatter(log_fmt))
        app.logger.addHandler(fh)
    else:
        app.debug_log_format = log_fmt
    open_config(app, config_file=config_file)

    setup_routes(app)
    return app
