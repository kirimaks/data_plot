#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import os.path
import sys
import time

tasks = [ config.cpu_temp, config.load_average, config.network_statistic ]


def get_data(file_data, cur_path):
    if __debug__:
        print u'\t<<%s>>' % cur_path

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


    # Return string for output file.
    return cur_line


def write_file(fp, cur_line):
    if __debug__:
        print 'Write: "%s" to "%s"' % (cur_line, fp)
    with open(fp, 'a') as out_file:
        out_file.write(cur_line)

# Return number of lines in a file.
def file_len(fp):
    num_lines = 0

    with open(fp) as fl:
        for line in fl:
            num_lines += 1

    if __debug__:
        print '\t\t%s : %d lines.' % (fp, num_lines)

    return num_lines


def truncate_file(fp):
    if file_len(fp) >= config.max_lines_in_file: 
        if __debug__:
            print '\t\tTruncate file: %s' % fp

        # OS specific code.
        if sys.platform == 'linux2':
            os.system('sed -i -e "1d" ' + fp)

def get_traffic(fp):
    traff1 = get_data(task, fp)
    time.sleep(1)
    traff2 = get_data(task, fp)

    return (int(traff2) - int(traff1)) / 1024



# Check work directory and create if need.
if not os.path.isdir(config.work_dir):
    if __debug__:
        print 'Create direcotry: %s' % config.work_dir
    os.mkdir(config.work_dir)


# Tasks.
for task in tasks:
    if __debug__:
        print u'*** %s ***' % task[u'title']

    out_file = cur_line = None

    # Network interfaces.
    if task[u'title'] == u'network_statistic':
        for iface in  task[u'ifaces']:  # Go for each interface.
            if __debug__:
                print u'\tRunning for: [%s]' % iface

            # Calculate paths.
            rx_path = os.path.join(task[u'path'][0], iface, task[u'path'][1], task[u'in_file'][0])
            tx_path = os.path.join(task[u'path'][0], iface, task[u'path'][1], task[u'in_file'][1])

            if __debug__:
                print u'\t\tRx path: "%s"' % rx_path
                print u'\t\tTx path: "%s"' % tx_path


            # Get current rx, tx in bytes per sec.
            cur_rx = get_traffic(rx_path)
            cur_tx = get_traffic(tx_path)

            if __debug__:
                print u'\t\t\t\tCurrent rx for [%s]: %d kB/s' % (iface, cur_rx)
                print u'\t\t\t\tCurrent tx for [%s]: %d kB/s' % (iface, cur_tx)

            # Create line for writing.
            cur_line = unicode(cur_rx) + u'\t' + unicode(cur_tx) + '\n'

            if __debug__:
                print u'String to write: %s' % cur_line

            # Setting path for output file.
            out_file = os.path.join( config.work_dir, unicode(iface) + u'_' + task[u'out_file'])

            write_file(out_file, cur_line)
            truncate_file(out_file)
            

    # Regular files.
    else:   
        path_to_file = os.path.join(task['path'], task['in_file'])
        cur_line = get_data(task, path_to_file)
        out_file = os.path.join(config.work_dir, task['out_file'])

        write_file(out_file, cur_line)
        truncate_file(out_file)

