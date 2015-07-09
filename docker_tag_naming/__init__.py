__VERSION__ = '1.0.6'


#
#   Disable requests logging
#
import logging

logging.getLogger('requests').setLevel(logging.WARNING)
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)