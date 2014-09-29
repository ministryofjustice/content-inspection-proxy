import os

from cip.application import app_maker

cfg = os.environ.get('CIP_CFG', '../config/config.yaml')
app = app_maker(config_file=cfg)

if __name__ == '__main__':
    app.run()
