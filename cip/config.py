"""
There is no value from having flask configuration separated from ianua configuration.
So let's have them both as a json file.
"""
import json

import yaml
from collections import OrderedDict


class UpperKeyLoader(yaml.Loader):
    pass


UpperKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: UpperKeyDict(loader.construct_pairs(node)))


class UpperString(str):
    def isupper(self):
        return True


class UpperKeyDict(OrderedDict):
    def __init__(self, mapping):
        new_mapping = [(UpperString(pair[0]), pair[1]) for pair in mapping]
        super(UpperKeyDict, self).__init__(new_mapping)


def open_config(app, config_file):
    global config
    with app.open_resource(config_file) as f:
        # we are using our loader as flask checks for keys in uppercase
        config = yaml.load(f.read(), UpperKeyLoader)
    app.config.from_object(type('', (object,), config))
