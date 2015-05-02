import sys
import logging

class Log_tool(object):
    
    #__defalut_debug_level = 20
    
    def __init__(self, debug_mode):
        debug_level = 10 if debug_mode else 20     # If debug_lever is fase, set 20 to debug mode.
        logging.basicConfig( level=debug_level, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%I:%M:%S' )

        if debug_mode:
            self.debug([u'Starting with debug mode.'])

    def info(self, args):
        logging.info(*args)

    def debug(self, args):
        logging.debug(*args)

    def error(self, args):
        logging.error(*args)

    def crit(self, args, exit_code = 1):   
        logging.critical(*args)
        sys.exit(exit_code)


