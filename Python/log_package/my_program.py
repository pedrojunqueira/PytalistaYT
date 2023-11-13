import logging

from mypackage import module


logging.basicConfig(level = logging.DEBUG, format = '%(levelname)s:%(asctime)s:%(name)s:%(message)s')
logging.getLogger(__name__)

log = logging.getLogger()

formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('my_program.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)
logging.getLogger('my_package.module').addHandler(file_handler)

module.do_something()

log.debug('This is a critical message')
log.critical('This is a critical message')




