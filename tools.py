#import logging as log
#log.basicConfig( level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%I:%M:%S' )
#log.basicConfig( level=config.debug_level, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%I:%M:%S' )

import time

time_begin = time.time()

#if __name__ == '__main__':
#    log.debug('Hello from (%s)', __file__)


#def create_table(cur, tab_name):
#    log.debug('Create table [%s]', tab_name)
#    cur.execute('CREATE TABLE ' + tab_name + '(Id INTEGER PRIMARY KEY, Time TEXT)')

#def add_column(cur, tab_name, col_name, col_type):
#    log.debug('Add column [%s] to table [%s]', col_name, tab_name)
#    cur.execute('ALTER TABLE ' + tab_name + ' ADD COLUMN ' + col_name + ' ' + col_type)

#def insert_into(cur, tab_name, col_name, data):
#    log.debug('Insert into table [%s], column [%s] - (%s)', tab_name, col_name, data)
#    cur.execute('INSERT INTO ' + tab_name + '(Time,' + col_name + ') ' + 'VALUES(datetime("now", "localtime"), ' + data + ')')

#def select_data(cur, tab_name, cols, rows_limit):
#    log.debug('Select %s from %s with limit: %d', cols, tab_name, rows_limit)
#    last_col = cols.split(',')[-1]
#    cur.execute('SELECT ' + cols + ' FROM ' + tab_name + ' WHERE ' + last_col + ' IS NOT Null' + ' ORDER BY ' + 'Id ' + 'DESC LIMIT ' + unicode(rows_limit))


#log.info('(%s) execution time: [%s]\n', __file__, time.time() - time_begin)


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



import sqlite3
import sys

class Db_tool(object):
    
    def __init__( self, db_file, log_tool ):
        log_tool.debug( [u'Open database file [%s]', db_file] )
        try:
            self.__conn = sqlite3.connect(db_file)
        except sqlite3.OperationalError:
            log_tool.debug( ['Create database file: [%s]', db_file] )
            self.__conn = None
            sys.exit(1)

    def __del__(self):
        if self.__conn:
            print u'Close database...'
            self.__conn.close()
        else:
            print u'Nothing to closing...'

    def create_table(cur, tab_name):
        pass

    def add_column(cur, tab_name, col_name, col_type):
        pass

    def insert_into(cur, tab_name, col_name, data):
        pass

    def select_data(cur, tab_name, cols, rows_limit):
        pass


if __name__ == u'__main__':
    log_tool = Log_tool(10)

    log_tool.info(['(%s) execution time: [%s]\n', __file__, time.time() - time_begin])
    log_tool.debug(['Select %s from %s with limit: %s', u'cols', u'tab_name', u'rows_limit'])
