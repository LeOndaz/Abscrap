import os
import logging
from .base import *

if os.environ['DEBUG'] == 'True':
    logging.info('RUNNING IN DEBUG MODE')
    from .dev import *
else:
    logging.info('RUNNING IN PRODUCTION MODE')
    from .prod import *
