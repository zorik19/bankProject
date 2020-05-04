from logging.config import dictConfig

from fwork.common.logs.logger import make_logger
from fwork.common.logs.settings import LOG_CONFIG

dictConfig(LOG_CONFIG)
get_logger = make_logger('lead_service')
