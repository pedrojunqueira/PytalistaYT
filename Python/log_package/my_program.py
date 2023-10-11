import logging

from mypackage import module

logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s:%(name)s:%(message)s')
logging.getLogger(__name__)

log = logging.getLogger()

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('my_program.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)
logging.getLogger('my_package.module').addHandler(file_handler)

module.do_something()

log.debug('debuggig something')
log.critical('critical root')



