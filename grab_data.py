#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import config
import os.path
import sys
import sqlite3

from tools import show_info

def prepare_db(dbfile):

    # Check file.
    if not os.path.isfile(dbfile):
        # Create database.
        try:
            if __debug__:
                show_info((u'Create database', config.dbfile))
            open(config.dbfile, u'w').close()
        except IOError, e:
            print u"Can't create file [%s]: %s" % (config.dbfile, e.args[1])
            sys.exit(1)

        # Create tables.
        try:
            if __debug__: show_info((u'Create tables', config.dbtables))

            db_conn = sqlite3.connect(dbfile)

            cur_conn = db_conn.cursor()

            for table in config.dbtables:

                if __debug__: show_info((u'Create table:', table), u'\t')

                field = None
                field_type = None
                
                if table == u'cpu_temp':
                    field = u'Temp'
                    field_type = u'REAL'
                elif table == u'load_average':
                    field = u'Data'
                    field_type = u'TEXT'

                cur_conn.execute(u'CREATE TABLE "%s"(Id INTEGER PRIMARY KEY, "%s" "%s", Date TEXT)' % (table, field, field_type))
                        

            db_conn.commit()
            db_conn.close()

        except sqlite3.Error, e:
            print u'Error :%s' % e.args[0]
            sys.exit(2)

        finally:
            if db_conn:
                db_conn.close()


def check_workdir():
    if not os.path.isdir(config.workdir):
        if __debug__: show_info((u'Create working directory', config.workdir))
        os.mkdir(config.workdir)


# Get data from file.
def get_data(task):
    cur_data = ''
    cur_path = os.path.join(task[u'path'], task[u'in_file'])

    if __debug__: show_info( (u'Open file', cur_path) , u'\t' )

    with open(cur_path) as cur_file:
        cur_data = cur_file.readline()

    # Prepare data for particular task.
    if task[u'title'] == u'cpu_temp':
        if __debug__: show_info( (u'Prepare data for', task[u'title']), u'\t' )
        cur_data = list(cur_data)
        cur_data.insert(2, u'.')
        cur_data.remove(u'\n')
        cur_data = u''.join(cur_data)

    elif task[u'title'] == u'load_average':
        if __debug__: show_info( (u'Prepare data for', task[u'title']), u'\t' )
        cur_data = cur_data[:14]

    return cur_data


# Write data to database.
def write_data(data, table):
    if __debug__: show_info((u'Write data for', task[u'title']), ending=u'[' + data + u']\n')

    conn = sqlite3.connect(config.dbfile)
    with conn:
        try:
            cur_conn = conn.cursor()

            field = None

            if table == u'cpu_temp':
                field = u'Temp'
            elif table == u'load_average':
                field = u'Data'

            #cur_conn.execute('INSERT INTO "%s"("%s") VALUES("%s")' % (table, field, data) )
            cur_conn.execute(u'INSERT INTO "%s"("%s","%s") VALUES("%s", datetime("now") )' % (table, field, u'Date', data) )

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
    if __debug__: show_info((u'Processing for', task[u'title']) )
    data = get_data(task)
    write_data(data, task[u'title'])
