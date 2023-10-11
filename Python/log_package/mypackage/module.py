import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

def do_something():
    log.debug('debuggig something')
    log.info('just info')
    log.warning('warning')
    log.error('Ooops error!')
    log.critical('Critical error! 😠')