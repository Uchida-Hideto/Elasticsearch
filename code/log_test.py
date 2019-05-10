import logging

# create log name and set log level
LOG = logging.getLogger('Paging_Search')
LOG.setLevel(level=logging.INFO)

# add handle to write
file_handler = logging.FileHandler(filename='search.log')
file_handler.setLevel(logging.DEBUG)

# add handler to terminal
# terminal_handler = logging.StreamHandler()
# terminal_handler.setLevel(logging.DEBUG)

# set log format
log_format = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(log_format)
# terminal_handler.setFormatter(log_format)

# add handler to log
LOG.addHandler(file_handler)
# LOG.addHandler(terminal_handler)

# log test
LOG.info('info test')
LOG.warning('warn test')
