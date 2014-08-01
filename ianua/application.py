from flask import Flask

from ianua.config import open_config
from ianua.pipeline import Pipeline


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
        #I guess we should initialize the object on start and we can make it a singleton
        #flask view classes - are they singletons? or should we have an independent storage
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
            app.add_url_rule(route_spec, "view{}".format(index), pipelines[pipeline_name],
                             strict_slashes=False,
                             methods=pipelines[pipeline_name].methods)

        app.logger.debug("Added route: {}".format(route))
        index += 1

    return app


def app_maker(config_file="../config/config.yaml"):
    app = Flask(__name__)

    app.debug_log_format = (
        '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
        '%(message)s\n'
    )

    open_config(app, config_file=config_file)
    setup_routes(app)
    return app
