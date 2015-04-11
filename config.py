#!/usr/bin/env python
# -*- coding: utf-8 -*-

dbfile = '/tmp/plot.db'
workdir = '/tmp/data_plot'
dbtables = ["cpu_temp", "load_average"]

cpu_temp = {
    'title'     :   'cpu_temp',
    'path'      :   '/sys/class/hwmon/hwmon0/',
    'in_file'   :   'temp1_input',
    'graph_file':   'cpu_temp.png'
}

load_average = {
    'title'    :   'load_average',
    'path'     :   '/proc',
    'in_file'  :   'loadavg',
    'graph_file':   'loadavg.png'
}

network_statistic = {
    'title'    :   'network_statistic',
    'ifaces'   :   ['lo', 'wlp1s0'],
    'path'     :   ['/sys/class/net/', 'statistics/'],
    'in_file'  :   ['rx_bytes', 'tx_bytes' ],
}

memory_statistic = {
    'title'     :   'memory_statistic',
    'path'      :   '/proc',     
    'in_file'   :   'meminfo'

}

cpu_usage = {
    'title'    :   'cpu_usage',
}

tasks = [ cpu_temp, load_average ]
