import logging

class Log_tool(object):
    
    def __init__(self, level=50):
        logging.basicConfig( level=level, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%I:%M:%S' )

    def info(self, args):
        logging.info(*args)

    def debug(self, args):
        logging.debug(*args)

    def error(self, args):
        logging.error(*args)

    def crit(self, args):
        logging.critical(*args)


