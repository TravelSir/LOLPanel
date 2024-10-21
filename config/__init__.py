import logging
import os

logger = logging.getLogger(__name__)

env = os.getenv('ENV')
try:
    if env == 'PRODUCTION':
        from .production import ProductionConfig as Config
        logging.info('Production config loaded.')
    else:
        from .test import TestConfig as Config
        logging.info('Testing config loaded.')
except ImportError:
    logging.warning('Loading config for %s environment failed, use test config instead.', env or 'unspecified')
    from .test import TestConfig as Config

COMMON_CONFIG = {
    'SWAGGER_CONFIG': {
        "debug": True,
        "headers": [
        ],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/api/lol/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/api/common/flasgger_static",
        # "static_folder": "static",  # must be set by user
        "swagger_ui": True,
        "specs_route": "/api/lol/apidocs/",
        "basePath": "/api/lol"
    }
}

for k, v in COMMON_CONFIG.items():
    setattr(Config, k, v)

