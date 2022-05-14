import os, sys, logging

os.chdir(os.path.dirname(__file__))
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


def log_errors(error):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    logger.error(f'''(at line: {str(exc_tb.tb_lineno)}) {str(error)} || TYPE: {str(exc_type)}''')