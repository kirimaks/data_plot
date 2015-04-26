#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import os.path

class Regular_File(object):
    
    def __init__(self, title, directory, input_file, graph_file):
        self.__title = title
        self.__dir = directory
        self.__in_file = input_file
        self.__graph_file = graph_file

    @property
    def file_path(self):
        return os.path.join(self.__dir, self.__in_file)

    @property
    def graph_path(self):
        return os.path.join(workdir, self.__graph_file)


class Network_Interface(Regular_File):
    def __init__(self, title, interface, directory_begin, directory_end, rx_file, tx_file, graph_file):
        Regular_File.__init__(self, title, None, None, graph_file )
        self.__interface = interface
        self.__dir_begin = directory_begin
        self.__dir_end = directory_end
        self.__rx_file = rx_file
        self.__tx_file = tx_file

    iface_name = property(lambda self: self.__interface)

    @property
    def rx_path(self):
        return os.path.join(self.__dir_begin, self.iface_name, self.__dir_end, self.__rx_file)

    @property
    def tx_path(self):
        return os.path.join(self.__dir_begin, self.iface_name, self.__dir_end, self.__tx_file)

        


if __name__ == u'__main__':
    cpu_temp = Regular_File(u'cpu_temp', u'/sys/class/hwmon/hwmon0/', u'temp1_input', u'cpu_temp.png')

    print u'Full path [%s]' % cpu_temp.file_path
    print u'Path to graph [%s]' % cpu_temp.graph_path

    wlan0 = Network_Interface(u'network_interface_wlan0', u'wlan0', u'/sys/class/net/', u'statistics/', u'rx_bytes', u'tx_bytes', u'wlan0_io.png')
    print u'\nFull path to rx file [%s]' % wlan0.rx_path
    print u'Full path to tx file [%s]' % wlan0.tx_path
    print u'Path to graph [%s]' % wlan0.graph_path


    eth0 = Network_Interface(u'network_interface_eth0', u'eth0', u'/sys/class/net/', u'statistics/', u'rx_bytes', u'tx_bytes', u'eth0_io.png')
    print u'\nFull path to rx file [%s]' % eth0.rx_path
    print u'Full path to tx file [%s]' % eth0.tx_path
    print u'Path to graph [%s]' % eth0.graph_path

