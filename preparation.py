import config
import os.path
import tools
import sys
import sqlite3

time_begin = tools.time.time()

def prepare_db(dbfile):

    if not os.path.isfile(dbfile):
        tools.log.debug('Create database: [%s]', dbfile)

        db_conn = sqlite3.connect(dbfile)

        try:
            open(config.dbfile, u'w').close()   # Create file.

            tools.log.debug(u'Create tables: (%s)', config.dbtables)

            cur_conn = db_conn.cursor()

            for table in config.dbtables:
                tools.create_table(cur_conn, table)

                # Create colums for specific task.
                if table == u'cpu_temp':
                    tools.add_column(cur_conn, table, col_name = u'Temp', col_type = u'REAL');

                elif table == u'load_average':
                    tools.add_column(cur_conn, table, col_name = u'min_1', col_type = u'REAL');
                    tools.add_column(cur_conn, table, col_name = u'min_5', col_type = u'REAL');
                    tools.add_column(cur_conn, table, col_name = u'min_15', col_type = u'REAL');
                
                elif table == u'network_statistic':
                    for iface in config.network_statistic['ifaces']:
                        tools.add_column(cur_conn, table, col_name = iface + u'_rx', col_type = u'INTEGER')
                        tools.add_column(cur_conn, table, col_name = iface + u'_tx', col_type = u'INTEGER')
                    

                        
            db_conn.commit()
            db_conn.close()



        except sqlite3.Error, e:
            print u'Error :%s' % e.args[0]
            sys.exit(2)

        finally:
            if db_conn:
                db_conn.close()


    # Check network columns.
    db_conn = sqlite3.connect(config.dbfile)
    column_list = []

    with db_conn:
        curs = db_conn.cursor()
        curs.execute('PRAGMA table_info(network_statistic)')
        
        # Get list of interfaces in database (column_list).
        tmp = curs.fetchone()
        while tmp != None:  
            if tmp[1] != u'Id' and tmp[1] != u'Time':
                iface = tmp[1][:-3]
                if iface not in column_list:
                    column_list.append(iface)
            tmp = curs.fetchone()

        table = u'network_statistic'
        # Check current list of interfaces and columns in the table.
        for iface in config.network_statistic[u'ifaces']:
            #print '[%s]' % iface
            if iface not in column_list:
                # Create table
                #print 'Create table for %s' % iface
                tools.add_column(curs, table, col_name = iface + u'_rx', col_type = u'INTEGER')
                tools.add_column(curs, table, col_name = iface + u'_tx', col_type = u'INTEGER')


#    sys.exit()



def check_workdir():
    if not os.path.isdir(config.workdir):
        tools.log.debug(u'Create working directory [%s]', config.workdir)
        os.mkdir(config.workdir)



tools.log.info('(%s) execution time: [%s]\n', __file__, tools.time.time() - tools.time_begin)
