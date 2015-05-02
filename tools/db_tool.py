import sqlite3
import os, os.path

class Db_tool(object):
    
    def __init__(self, db_dir, log_tool):
        self.__log_tool = log_tool
        self.__db_file  = u'data.db'    # Default database file name.
        self.__db_path  = os.path.join(db_dir, self.__db_file)

        if not os.path.isfile(self.__db_path) or not os.path.isdir(db_dir):
            self.initdb(db_dir, self.__db_path)

    def initdb(self, db_dir, db_path):
        self.__log_tool.info( [u'Create new database in [%s]', db_path] )

        #------------- Create working directory and database file. ----------------------------
        try:
            self.__log_tool.debug([u'Creating working directory [%s]', db_dir])
            os.mkdir(db_dir) 
        except Exception as Exc:
            if Exc.args[1] == u'File exists':
                self.__log_tool.error([u'Working direcotry [%s] exist.', db_dir])
            else:
                self.__log_tool.crit([u'[%s], exit...', Exc.args[1]])

        try:
            self.__log_tool.debug([u'Creating database file %s/[%s]', db_dir, self.__db_file])
            open(db_path, u'w').close()
        except Exception as Exc:
                self.__log_tool.crit([u'[%s], exit...', Exc.args[1]])
        #--------------------------------------------------------------------------------------

        #-------------- Create necessary tables. ----------------------------------------------
        self.create_table(  u'CpuTemp', 
                            Id          = u'INTEGER PRIMARY KEY', 
                            Time        = u'TEXT',
                            Sensor0     = u'REAL', 
                            Sensor1     = u'REAL', 
                            Sensor2     = u'REAL', 
                            Sensor3     = u'REAL', 
                            Sensor4     = u'REAL', 
                            Sensor5     = u'REAL', 
                            Sensor6     = u'REAL', 
                            Sensor7     = u'REAL' 
        )
        self.create_table(  u'LoadAverage', 
                            Id          = u'INTEGER PRIMARY KEY', 
                            Load_1min   = u'REAL', 
                            Load_5min   = u'REAL', 
                            Load_15min  = u'REAL', 
                            Time        = u'TEXT' 
        )
        self.create_table(  u'Network_Interfaces', 
                            Id      = u'INTEGER PIRMARY KEY', 
                            Name    = u'TEXT' 
        ) 
        self.create_table(  u'Network_Statistic', 
                            Id          = u'INTEGER PRIMARY KEY', 
                            InterfaceId = u'INTEGER',
                            rx_io       = u'INTEGER',  
                            tx_io       = u'INTEGER',
                            pkg_rx      = u'INTEGER', 
                            pkg_tx      = u'INTEGER',
                            err_rx      = u'INTEGER', 
                            err_tx      = u'INTEGER' 
        ) 
        #--------------------------------------------------------------------------------------


    @property
    def db_path(self):
        return sqlite3.connect(self.__db_path)

    def create_table(self, tab_name, **fields):
        self.__log_tool.debug([ u'Create table [%s]', tab_name ])

        #----------- Create string with fields and types. ------------
        field_string = '('
        for (Field, Type) in fields.iteritems():
            if len(field_string) > 1:
                field_string += ', ' 
            field_string += Field + ' ' + Type
        field_string += ')'
        #-------------------------------------------------------------

        cmd = u'CREATE TABLE ' + tab_name + u' ' + field_string

        with self.db_path as conn:
            cur = conn.cursor()
            cur.execute(cmd)

    def add_column(self, tab_name, col_name, col_type):
        with self.db_path as conn:
            cur = conn.cursor()
            cur.execute('')

    def insert_into(self, tab_name, fields, values):
        with self.db_path as conn:
            cur = conn.cursor()
            cmd = u'INSERT INTO ' + tab_name + fields + u' VALUES' + values
            #self.__log_tool.debug(['%s', cmd])
            cur.execute(cmd)

    def select_data(self, tab_name, cols, rows_limit):
        with self.db_path as conn:
            cur = conn.cursor()
            cur.execute('')

if __name__ == u'__main__':
    print u'Test'
