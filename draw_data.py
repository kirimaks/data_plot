#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sqlite3
import config
import tools
import argparse
from drawing import draw_data

time_begin = tools.time.time()

def get_data_from_db(task, cur_con, rows_limit, tab_col = None):
    
    data = { 
        u'Time': [], 
        u'f1'  : [],
        u'f2'  : [], 
        u'f3'  : [], 
        u'f4'  : [],
    }

    if task[u'title'] == u'cpu_temp':
        tools.select_data(cur_con, task[u'title'], u'Time,Temp', rows_limit)

        tmp = cur_con.fetchone()
        while tmp != None:
            data[u'Time'].insert(0,tmp[0])
            data[u'f1'].insert(0,tmp[1])
            tmp = cur_con.fetchone()


    elif task[u'title'] == u'load_average':
        tools.select_data(cur_con, task[u'title'], u'Time,min_1,min_5,min_15', rows_limit)

        tmp = cur_con.fetchone()
        while tmp != None:
            data[u'Time'].insert(0,tmp[0])
            data[u'f1'].insert(0,tmp[1])
            data[u'f2'].insert(0,tmp[2])
            data[u'f3'].insert(0,tmp[3])
            tmp = cur_con.fetchone()


    elif task[u'title'] == u'network_statistic':

        for fl in task[u'in_file']:
            cur_col = tab_col + '_' + fl[0:2]
            tools.select_data(cur_con, task[u'title'], u'Time,' + cur_col, rows_limit)

            tmp = cur_con.fetchone()
            while tmp != None:
                if fl == u'rx_bytes':
                    data[u'Time'].insert(0,tmp[0])
                    data[u'f1'].insert(0,tmp[1])
                else:
                    data[u'f2'].insert(0,tmp[1])

                tmp = cur_con.fetchone()
                

    return data



parser = argparse.ArgumentParser(description=u'Create graphics.', epilog=u'The End.')
parser.add_argument(u'-m', type=int, default=120, help=u'set how many minutes to show.')
cmdargs = parser.parse_args()


tools.log.info(u'Show for %d minutes.', cmdargs.m)


try:
    tools.log.debug(u'Connect to: [%s]\n', config.dbfile) 
    conn = sqlite3.connect(config.dbfile)

    with conn:
        cur_con = conn.cursor()

        for task in config.tasks:
            tools.log.info(u'Processing for (%s)', task[u'title'])

            if task[u'title'] == u'network_statistic':
                for iface in task[u'ifaces']:
                    data = get_data_from_db(task, cur_con, cmdargs.m, tab_col = iface)
                    #print data
                    draw_data(data, task, cmdargs.m, tab_col = iface)

            else:
                data = get_data_from_db(task, cur_con, cmdargs.m)
                draw_data(data, task, cmdargs.m)


except sqlite3.Error, e: 
    print u'Error %s:', e.args[0]
    sys.exit(1)

finally:
    if conn: conn.close()



tools.log.info('(%s) execution time: [%s]\n', __file__, tools.time.time() - tools.time_begin)
