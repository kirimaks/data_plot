#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import config
import os.path
import sys
import sqlite3
import tools
from preparation import prepare_db, check_workdir

time_begin = tools.time.time()

def read_file(fp):
    tools.log.debug(u'Open file: [%s]', fp)

    with open(fp) as cur_file:
        cur_data = cur_file.readline()

    return cur_data

# Get data from file.
def get_data(task, cur_path):
    cur_data = u''

    tools.log.debug(u'Prepare data for: [%s]', task[u'title'])

    cur_data = read_file(cur_path)

    # Prepare data for particular task.
    if task[u'title'] == u'cpu_temp':
        cur_data = list(cur_data)
        cur_data.insert(2, u'.')
        cur_data.remove(u'\n')
        cur_data = u''.join(cur_data)

    elif task[u'title'] == u'load_average':
        cur_data = cur_data[:14]

    return cur_data

def get_net_data(fp, iface):
    sc = 1
    cur_data = u''
    tools.log.debug(u'Prepare network data for: [%s]', iface)

    d1 = read_file(fp)
    tools.log.info('Waiting %dsec.', sc)
    tools.time.sleep(sc)
    d2 = read_file(fp)

    cur_data = (int(d2) - int(d1)) / 1024
    
    return cur_data


# Write data to database.
def write_data(data, table, tab_col = None):
    tools.log.debug(u'Write data (%s) for [%s]', data, task[u'title'])

    conn = sqlite3.connect(config.dbfile)
    with conn:
        try:
            cur_conn = conn.cursor()

            if table == u'cpu_temp':
                tools.insert_into( cur_conn, table, u'Temp', data )

            elif table == u'load_average':
                data = data.split(' ')
                data_str = data[0] + ',' + data[1] + ',' + data[2]
                tools.insert_into( cur_conn, table, u'min_1,min_5,min_15', data_str )

            elif table == u'network_statistic':
                tools.insert_into( cur_conn, table, tab_col, str(data))
                

            conn.commit()

        except sqlite3.Error, e:
            print u'Database error: %s' % e.args[0]
            sys.exit(1)

        finally:
            if cur_conn:
                cur_conn.close()


check_workdir()
prepare_db(config.dbfile)


for task in config.tasks:
    data = None
    tools.log.info(u'Processing for: [%s]', task[u'title'])

    if task[u'title'] == 'network_statistic':
        for iface in config.network_statistic[u'ifaces']:
            for stat_fl in task[u'in_file']:
                data = get_net_data(os.path.join(task[u'path'][0], iface, task[u'path'][1], stat_fl), iface)
                write_data(data, task[u'title'], tab_col = iface + '_' + stat_fl[:2])

    else:
        data = get_data(task, os.path.join(task[u'path'], task[u'in_file']))
        write_data(data, task[u'title'])




tools.log.info('(%s) execution time: [%s]\n', __file__, tools.time.time() - tools.time_begin)
