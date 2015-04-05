#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import os.path
import sys


tasks = [ config.cpu_temp, config.load_average, config.network_statistic ]


def regular_file(file_data):
    if __debug__:
        print u'\t<<%s>>(regular file)' % file_data[u'in_file']

    cur_path = os.path.join(file_data[u'path'], file_data[u'in_file'])
    cur_line = None


    # Reading.
    with open(cur_path) as cur_file:
        cur_line = cur_file.readline()
        if __debug__:
            print u'\t\t%s' %  cur_line


    # Prepare line for different tasks.
    if file_data[u'title'] == u'cpu_temp':
        cur_line = list(cur_line)
        cur_line.insert(2, u'.')
        cur_line = ''.join(cur_line)


    # Writing.
    cur_path = os.path.join(config.work_dir, file_data['out_file'])
    with open(cur_path, 'a') as out_file:
        out_file.write(cur_line)



# Return number of lines in a file.
def file_len(f):
    num_lines = 0

    with open(f) as fl:
        for line in fl:
            num_lines += 1

    if __debug__:
        print '\t\t%s : %d lines.' % (f, num_lines)

    return num_lines



def truncate_file(f):
    if file_len(f) >= config.max_lines_in_file: 
        if __debug__:
            print '\t\tTruncate file: %s' % f

        # OS specific code.
        if sys.platform == 'linux2':
            os.system('sed -i -e "1d" ' + f)
            



# Check work directory and create if need.
if not os.path.isdir(config.work_dir):
    if __debug__:
        print 'Create direcotry: %s' % config.work_dir
    os.mkdir(config.work_dir)




################
# Main program #
################

for task in tasks:
    if __debug__:
        print '*** %s ***' % task[u'title']

    if task[u'title'] == 'network_statistic':
        for iface in  task[u'ifaces']:
            print '\t[%s]' % iface
    else:
        regular_file(task)
        # Use truncate only for regular temporary.
        truncate_file(os.path.join(config.work_dir, task[u'out_file']))
