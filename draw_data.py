#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

time_begin = time.time()

import tools
import argparse
import task_types
import ConfigParser


def arguments_analysis():
    args = argparse.ArgumentParser(description=u'Reading database and create graphics.')
    args.add_argument(u'-v', '--version',         action=u'version',     version='%(prog)s 2.0')
    args.add_argument(u'-d', dest=u'debug_mode',  action=u'store_true',  help=u'Debug mode (default mode is INFO).')
    args.add_argument(u'-c', dest=u'config_file', metavar=u'config.cfg', required=True, help=u'Configuration file.')
    cmdargs = args.parse_args()

    return args.parse_args()


def config_analysis(config_file):
    config = ConfigParser.RawConfigParser()
    config.read(config_file)

    return config


if __name__ == '__main__':
    
    #------------- Preparations. ----------------------------------------------------------
    cmdargs  = arguments_analysis()
    conf     = config_analysis(cmdargs.config_file)
    log_tool = tools.Log_tool(cmdargs.debug_mode)
    db_tool  = tools.Db_tool(db_dir = conf.get(u'Basic', u'workdir'), log_tool = log_tool)
    #--------------------------------------------------------------------------------------

    
    for cur_task in conf.sections()[1:]:
        log_tool.debug([u'Processing for [%s]', cur_task])

        ### Processing for network interface. ###
        if cur_task in conf.get(u'Basic', u'network_interfaces'): 
            net_task = task_types.Network_Task( cur_task, conf, log_tool, db_tool )
            net_task.retrive_data()
            net_task.draw_data()
        
        ### Processing for regular file. ###
        else:
            reg_task = task_types.Regular_Task( cur_task, conf, log_tool, db_tool )
            reg_task.retrive_data()
            reg_task.draw_data()

    log_tool.debug(['(%s) execution time: [%s]', __file__, time.time() - time_begin])
