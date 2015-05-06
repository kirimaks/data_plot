#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re

class CpuTemp(object):

    # Reading and preparing data for CpuTemp task.
    @staticmethod
    def get_data(config_file, log_tool):
        ''' Reading data from file. '''
        
        #---------- Create list of sensors. -------------------------------------
        sensors = {}
        sensors_pattern = re.compile(u'sensor\d')

        for section in list(config_file.items(u'CpuTemp')):
            if sensors_pattern.search(section[0]):
                sensors[section[0]] = section[1]
        #------------------------------------------------------------------------

        #----------- Reading for every sensors and store data. ------------------
        temp_data = {}
        for (sensor_name, sensor_file) in sensors.iteritems():
            try:
                with open(sensor_file) as sf:
                    data = list(sf.readline().rstrip())

                data.insert(2,u'.')
                temp_data[sensor_name] = ''.join(data)

            except Exception as Exc:
                log_tool.crit([u'[%s] %s, exit...', Exc.filename, Exc.args[1] ])
        #------------------------------------------------------------------------

        return temp_data


    @staticmethod
    def write_data(tab_name, cur_data, db_tool, log_tool): # Inherided in LoadAverage.
        ''' Write data to database. '''

        #----------- Calculate string for insertion -----------------
        fields = u'('
        values = u'('

        for k in cur_data.keys():
            if len(fields) > 1:
                fields += u', '
            if len(values) > 1:
                values += u', '
            fields += k
            #values += cur_data[k]
            values += unicode(cur_data[k])

        fields += u', Time'
        values += u", time('now', 'localtime')"

        fields += u')'
        values += u')'
        #------------------------------------------------------------

        db_tool.insert_into( tab_name, fields, values )

    
    @staticmethod
    def read_db_data(db_tool, conf):
        ''' Reading data of database, and create dict with data. '''

        cpu_temp_data = {}

        # TODO: ---- Get sensors number. ---------------------------
        #data = conf.items(u'CpuTemp') 
        number_of_sensors = 0
        sensors_pattern = re.compile(u'sensor\d')
        for item in conf.items(u'CpuTemp'):
            if sensors_pattern.search(item[0]):
                number_of_sensors += 1

        ##
        print number_of_sensors
        ##
            
        #-----------------------------------------------------------
    

class LoadAverage(CpuTemp):
    
    @staticmethod
    def get_data(config_file, log_tool):
        ''' Read data from file. '''

        load_avg_data = {}

        try:
            with open(config_file.get( u'LoadAverage', u'load_file' )) as LoadFile:
                data = LoadFile.readline()

        except Exception as Exc:
            log_tool.crit([u'[%s] %s, exit...', Exc.filename, Exc.args[1] ])
        
        data = data.split(' ')
        load_avg_data[u'Load_1min']  = data[0]
        load_avg_data[u'Load_5min']  = data[1]
        load_avg_data[u'Load_15min'] = data[2]

        return load_avg_data





class Regular_Task(object):
    # Regular task, just read data from one file.

    known_regular_tasks = [u'CpuTemp', u'LoadAverage']
    
    def __init__(self, task_name, config, log_tool, db_tool):

        if task_name not in Regular_Task.known_regular_tasks:
            log_tool.crit([u'Unknown task: [%s].', task_name])

        self.__task_name    = task_name
        self.__config       = config
        self.__log_tool     = log_tool
        self.__db_tool      = db_tool


    #----------------- Methods for store data to database. ----------------------------------------------------------
    #def read_data(self):
    def reading_data_from_file(self):
        self.__log_tool.debug([u'Reading data for [%s] task.', self.__task_name])

        if self.__task_name == u'CpuTemp':
            self.__cur_data = CpuTemp.get_data(self.__config, self.__log_tool)  # Hold the dictionary with data.

        elif self.__task_name == u'LoadAverage':
            self.__cur_data = LoadAverage.get_data(self.__config, self.__log_tool)


    #def write_data(self):
    def write_data_to_db(self):
        self.__log_tool.debug([u'Write data for [%s] task.', self.__task_name])

        if self.__task_name == u'CpuTemp':
            CpuTemp.write_data( u'CpuTemp', self.__cur_data, self.__db_tool, self.__log_tool )

        elif self.__task_name == u'LoadAverage':
            LoadAverage.write_data( u'LoadAverage', self.__cur_data, self.__db_tool, self.__log_tool )
    #----------------------------------------------------------------------------------------------------------------


    #----------------- Methods for retrive data from database. ------------------------------------------------------
    def retrive_data(self):
        self.__log_tool.debug( [u'Retrive data for [%s] task.', self.__task_name] )

        if self.__task_name == u'CpuTemp':
            self.__cur_data = CpuTemp.read_db_data( self.__db_tool, self.__config )

    def draw_data(self):
        self.__log_tool.debug( [u'Drawing data for [%s] task.', self.__task_name] )
    #----------------------------------------------------------------------------------------------------------------

