import sqlite3
import sys

class Db_tool(object):
    
    # TODO: In sqlite need open and close db in one queue.
    def __init__(self, db_file, log_tool):
        self.__db_file = db_file
        self.__log_tool = log_tool

    # TODO: Check if file exist here, and create if need.
    # NOTE: Sqlite3 creates file if not exist. 

    #def open_db(self):
    #    log_tool.debug( [u'Opening database file [%s]', db_file] )
    #    self.__conn = sqlite3.connect(self.__db_file)
    #    self.__cur = conn.cursor()
            
    # NOTE: Content manager makes conn.commit() and conn.exit() automatically.

    #def close_db(self):
    #    self.__conn.commit()
    #    self.__conn.close()

    @classmethod
    def db_path(self):
        return sqlite3.connect(self.__db_file)

    def create_table(self, self.__cur, tab_name):
        with Db_tool.db_path() as conn:
            cur = conn.cursor()
            cur.execute('')

    def add_column(self, self.__cur, tab_name, col_name, col_type):
        with Db_tool.db_path() as conn:
            cur = conn.cursor()
            cur.execute('')

    def insert_into(self, self.__cur, tab_name, col_name, data):
        with Db_tool.db_path() as conn:
            cur = conn.cursor()
            cur.execute('')

    def select_data(self, self.__cur, tab_name, cols, rows_limit):
        with Db_tool.db_path() as conn:
            cur = conn.cursor()
            cur.execute('')

if __name__ == u'__main__':
    print u'Test'
