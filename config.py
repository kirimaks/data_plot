#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Working directory
work_dir = u'/tmp/data_plot'

# Number of lines in output files.
max_lines_in_file = 14 

cpu_temp = {
    u'title'    :   u'cpu_temp',
    u'path'     :   u'/sys/class/hwmon/hwmon0/',
    u'in_file'  :   u'temp1_input',
    u'out_file' :   u'cpu_temp.txt'
}

load_average = {
    u'title'    :   u'load_average',
    u'path'     :   u'/proc',
    u'in_file'  :   u'loadavg',
    u'out_file' :   u'loadavg.txt'
}

network_statistic = {
    u'title'    :   u'network_statistic',
    u'ifaces'   :   [u'lo', u'wlp1s0'],
    u'path'     :   [u'/sys/class/net/', u'statistics/'],
    u'in_file'  :   [u'rx_bytes', u'tx_bytes' ],
    u'out_file' :   u'traffic.txt'
}

memory_statistic = {
    u'title'    :   u'memory_statistic',
    u'out_file' :   u'memory.txt'
}

cpu_usage = {
    u'title'    :   u'cpu_usage',
    u'out_file' :   u'cpu_usage.txt'
}

tasks = [ cpu_temp, load_average, network_statistic, memory_statistic, cpu_usage ]
