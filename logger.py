'''
=== USAGE ===

from logger import logger, log_traces

logger.info(...)
logger.error(...)

'''

import os, sys, logging, traceback

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('__VENDORS')

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


def log_traces():
    logger.error(traceback.format_exc())