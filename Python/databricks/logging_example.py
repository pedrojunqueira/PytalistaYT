import logging
import time
import datetime

logfile_prefix = 'my_logger'
file_date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
log_dir = '/tmp/'
log_file_name = f'{logfile_prefix}_{file_date}.log'
log_file = f'{log_dir}{log_file_name}'
log_file = f"/mnt/databricks/logs/{log_file_name}"
logger = logging.getLogger('custom_log')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, mode='a')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
if logger.hasHandlers():
    logger.handlers.clear()

# add handlers

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.debug("starting_log")

dbutils.fs.mv(f'file:{log_file}',f"dbfs:/mnt/databricks/logs/{log_file_name}")