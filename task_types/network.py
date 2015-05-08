#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import tools
import os.path
import regular  # Write_data function.

class Network_File(regular.CpuTemp):
    # Need write_data method from CpuTemp.

    @staticmethod
    def get_interface_id(interface, db_tool, log_tool ):
        
        data = db_tool.select_data_where( u'Network_Interfaces', u'Name, Id', u'Name', interface ).fetchone()

        if data == None:
            # Create a record about interface.
            log_tool.debug([u'Create record for [%s] interface.', interface])
            field = u'(Name)'
            value = u'("' + unicode(interface) + u'")'
            db_tool.insert_into(u'Network_Interfaces', field, value)
            data = db_tool.select_data_where( u'Network_Interfaces', u'Name, Id', u'Name', interface ).fetchone()

        if len(data) == 0:
            log_tool.crit([u"Can't get information from database."])

        return data

    @staticmethod
    def read_db_data( db_tool, conf, interface ):
        ''' Reading data from database, and create dict with data (For network). '''

        network_data = { u'Time' : [] }
        fields = u'Time'

        stat_types = conf.get( u'Basic', u'network_stat_types' ).split()

        for stat_type in stat_types:
            if u'bytes' in stat_type:
                fields += u',rx_bytes,tx_bytes'
                network_data[u'rx_bytes'] = []
                network_data[u'tx_bytes'] = []

            elif u'packets' in stat_type:
                fields += u',rx_packets,tx_packets'
                network_data[u'rx_packets'] = []
                network_data[u'tx_packets'] = []

            elif u'errors' in stat_type:
                fields += u',rx_errors,tx_errors'
                network_data[u'rx_errors'] = []
                network_data[u'tx_errors'] = []

        fields += u',Network_Statistic.Id'
        fields_list = fields.rsplit(u',')

        for row in db_tool.select_for_interface( fields, interface ):
            n = 0
            for field in fields_list:
                if field != u'Network_Statistic.Id':
                    network_data[field].insert(0,row[n])
                    n += 1

        return network_data
    

class Network_Task(object):

    known_types = [u'bytes', u'packets', u'errors']

    def __init__( self, cur_task, config_file, log_tool, db_tool ):
        self.__interface = cur_task
        self.__log_tool  = log_tool
        self.__db_tool   = db_tool
        self.__config    = config_file

        self.__network_data = {}


    #------------------ Store data. ---------------------------------------------------------------------------------
    def reading_data_from_file(self):
        # Reading data from network interface.

        list_of_stat_types = self.__config.get(u'Basic', u'network_stat_types').split(u',')

        for stat_type in list_of_stat_types:
            stat_type = stat_type.strip()

            if stat_type not in self.known_types: 
                self.__log_tool.crit( [u'Unknown statistic type [%s]', stat_type] )
            
            # Create path to network file.
            for io_path in [ u'rx_', u'tx_' ]:
                full_path = os.path.join(u'/sys/class/net/', self.__interface, u'statistics', io_path + stat_type) 

                data1 = data2 = 0

                try:
                    with open(full_path) as fp:
                        data1 = int(fp.readline())
                        fp.seek(0)
                        time.sleep(1)
                        data2 = int(fp.readline())

                except IOError as Exc:
                    self.__log_tool.crit([u'[%s], %s', Exc.filename, Exc.args[1] ])
                    
                data = int(data2 - data1)

                data = 0 if data < 0 else data

                self.__network_data[io_path + stat_type] = data / 1024 if stat_type == u'bytes' else data


    def write_data_to_db(self):
        # Get interfaces id.
        Interface_data = Network_File.get_interface_id( self.__interface, self.__db_tool, self.__log_tool )

        self.__network_data[u'InterfaceId'] = Interface_data[1]

        # Write network_data.
        Network_File.write_data( u'Network_Statistic', self.__network_data, self.__db_tool, self.__log_tool )
    #----------------------------------------------------------------------------------------------------------------


    #--------- Retrive and draw data. -------------------------------------------------------------------------------
    def retrive_data(self):
        self.__log_tool.debug([u'Retrive data for [%s]', self.__interface])
        self.__cur_data = Network_File.read_db_data( self.__db_tool, self.__config, self.__interface )
        
    def draw_data(self):
        self.__log_tool.debug( [u'Rrawing data for [%s]', self.__interface] )
        minuts = self.__db_tool.minuts_limit
        figure = tools.Drawing( self.__interface, self.__cur_data, self.__config, self.__log_tool, minuts )
        figure.create_graph()
    #----------------------------------------------------------------------------------------------------------------


