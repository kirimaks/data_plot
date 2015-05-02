#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read(u'../config.cfg')

for task in config.sections()[1:]:
    print task

    try:
        print u'Types: %s' % unicode(config.get(task, u'types'))
    except ConfigParser.NoOptionError:
        pass

    if task in config.get(u'Basic', u'network_interfaces'):
        print u'network:'
    
    print u'Graph: [%s]\n' % config.get(task, u'graph_file')
