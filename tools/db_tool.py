import sqlite3
import os, os.path
import re

class Db_tool(object):
    # TODO: Add truncate_db method (keep database small size).
    
    def __init__(self, db_dir, log_tool, config_file, recreate_db):
        self.__log_tool = log_tool
        self.__db_file  = u'data.db'    # Default database file name.
        self.__db_path  = os.path.join(db_dir, self.__db_file)
        self.__conf     = config_file

        if not os.path.isfile(self.__db_path) or not os.path.isdir(db_dir) or recreate_db:
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
        # TODO: generage sensors list from file. 

        ### Calculate number of sensors ###
        db_string = { u'Id' : u'INTEGER PRIMARY KEY', u'Time' : u'TEXT' } 

        # TODO: test about sensorN lower and upper case.
        sensors_pattern = re.compile(u'sensor\d')
        for item in self.__conf.items(u'CpuTemp'):
            if sensors_pattern.search(item[0]):
                db_string[item[0]] = u'REAL'

        self.create_table( u'CpuTemp', **db_string )

        '''
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
        '''

        self.create_table(  u'LoadAverage', 
                            Id          = u'INTEGER PRIMARY KEY', 
                            Load_1min   = u'REAL', 
                            Load_5min   = u'REAL', 
                            Load_15min  = u'REAL', 
                            Time        = u'TEXT' 
        )
        self.create_table(  u'Network_Interfaces', 
                            Id      = u'INTEGER PRIMARY KEY', 
                            Name    = u'TEXT' 
        ) 
        self.create_table(  u'Network_Statistic', 
                            Id          = u'INTEGER PRIMARY KEY', 
                            InterfaceId = u'INTEGER',
                            rx_bytes    = u'INTEGER',  
                            tx_bytes    = u'INTEGER',
                            rx_packets  = u'INTEGER', 
                            tx_packets  = u'INTEGER',
                            rx_errors   = u'INTEGER', 
                            tx_errors   = u'INTEGER', 
                            Time        = u'TEXT'
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

        self.__log_tool.debug( [ u'[%s]', cmd ] )

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
            self.__log_tool.debug(['%s', cmd])
            try:
                cur.execute(cmd)
            except sqlite3.OperationalError as Exc:
                self.__log_tool.crit([u'%s. Use --initdb for recreate database.', Exc.message])

    def select_data_where( self, tab_name, col, where_col, where_pattern):
        with self.db_path as conn:
            cur = conn.cursor()
            cmd = u'SELECT ' + col + u' FROM ' + tab_name + u' WHERE ' + where_col + u' == ' + '"' + where_pattern + '"'
            self.__log_tool.debug(['%s', cmd])
            return cur.execute(cmd)

if __name__ == u'__main__':
    print u'Test'
