#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os.path

class Network_File(object):
    pass

class Network_Task(object):

    known_types = [u'bytes', u'packets', u'errors']

    def __init__( self, cur_task, config_file, log_tool, db_tool ):
        self.__interface = cur_task
        self.__log_tool  = log_tool
        self.__db_tool   = db_tool
        self.__config    = config_file

        self.__iface_stat_data = {}


    def read_data(self):
        list_of_stat_types = self.__config.get(u'Basic', u'network_stat_types').split(u',')

        for stat_type in list_of_stat_types:
            stat_type = stat_type.strip()

            if stat_type not in self.known_types: 
                self.__log_tool.crit( [u'Unknown statistic type [%s]', stat_type] )
            
            # Create path to network file.
            for io_path in [ u'rx_', u'tx_' ]:
                full_path = os.path.join(u'/sys/class/net/', self.__interface, u'statistic', io_path + stat_type) 
                print full_path


    def write_data(self):
        pass

