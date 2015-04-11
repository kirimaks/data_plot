#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sqlite3
import config
from tools import show_info
import argparse
from drawing import draw_data

def select_data(task, cur_con):
    cur_con.execute(u'SELECT * FROM "%s" LIMIT (select count(*) - %d FROM %s), (select count(*) from %s)' % \
                    ( task[u'title'], cmdargs.m, task[u'title'], task[u'title']) )

    cur_row = cur_con.fetchone()
    data = []
    x = []
    y = []
    z = []

    while cur_row != None:
        # Prepare data for particular task.

        if task[u'title'] == u'cpu_temp':
            data.append(cur_row[1])
            cur_row = cur_con.fetchone()

        elif task[u'title'] == u'load_average':
            cur_str = cur_row[1].split(u' ')

            x.append(cur_str[0])
            y.append(cur_str[1])
            z.append(cur_str[2])

            cur_row = cur_con.fetchone()

            if cur_row == None:
                data.append(x)
                data.append(y)
                data.append(z)

    return data


parser = argparse.ArgumentParser(description=u'Create graphics.', epilog=u'The End.')
parser.add_argument(u'-m', type=int, default=121, help=u'set how many minutes to show.')
cmdargs = parser.parse_args()
if __debug__: show_info((u'Show minutes', cmdargs.m)) 


try:
    if __debug__ : show_info( (u'Connect to', config.dbfile) )
    conn = sqlite3.connect(config.dbfile)

    with conn:
        cur_con = conn.cursor()

        for task in config.tasks:
            if __debug__ : show_info((u'Processing for', task[u'title']))

            data = select_data(task, cur_con)
            draw_data(data, task, cmdargs.m)


except sqlite3.Error, e: 
    print u'Error %s:', e.args[0]
    sys.exit(1)

finally:
    if conn: conn.close()
