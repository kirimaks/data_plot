import tools

import matplotlib
matplotlib.use(u'Agg')

import matplotlib.pyplot as plt
import os.path
import config

def prepare_time(t):
    time = []

    first_elem = 0
    last_elem = len(t)-1
    mid_elem = last_elem/2
    first_part = mid_elem/2
    last_part = mid_elem + first_part

    time.append(t[first_elem][11:-3])
    time.append(t[first_part][11:-3])
    time.append(t[mid_elem][11:-3])
    time.append(t[last_part][11:-3])
    time.append(t[last_elem][11:-3])

    return time


def draw_data(data, task, minuts, tab_col = None ):
    save_destination = None

    # Lenght of graph.
    #x = [ t for t in range(minuts) ]
    #x = None
    #if len(data[u'Time']) < minuts:
    #    x = [ t for t in range(len(data[u'Time'])) ]
    #else:
    #    x = [ t for t in range(minuts) ]

    if len(data[u'Time']) < minuts:
        minuts = len(data[u'Time'])

    x = [ t for t in range(minuts) ]
    
    #print len(data[u'Time'])
    #print minuts

    # Calculate time.
    time = prepare_time(data[u'Time'])
    ax = plt.gca()
    time_range = range(-1, minuts, minuts/4)
    time_range[0] = 0
    ax.set_xticks(time_range)
    ax.set_xticklabels(time)

    titleis = task[u'title']

    if task[u'title'] == u'cpu_temp':
        save_destination = os.path.join(config.workdir, task[u'graph_file'])

        ylabelis = u'Temperature C'
        plt.plot(x, data[u'f1'], u'k', label=u'Temperature')
        plt.fill_between(x, data[u'f1'], 0, color=u'red', alpha='0.8')
        plt.yticks(range(5,101, 5))

    elif task[u'title'] == u'load_average':
        save_destination = os.path.join(config.workdir, task[u'graph_file'])

        ylabelis = u'Load Average'
        plt.plot(x, data[u'f1'], u'r', label=u'1 minut')
        plt.plot(x, data[u'f2'], u'b', label=u'5 minuts')
        plt.plot(x, data[u'f3'], u'g', label=u'15 minuts')

        # Fill for 15 minuts.
        plt.fill_between(x, data[u'f3'], 0, color=u'green', alpha='0.8')

    elif task[u'title'] == u'network_statistic':
        save_destination = os.path.join(config.workdir, tab_col + '_io.png')

        titleis = task[u'title'] + ': [' + tab_col + ']'

        ylabelis = u'kB/s: [%s]' % tab_col
        plt.plot(x, data[u'f1'], u'g-', label=u'RX')
        plt.plot(x, data[u'f2'], u'b-', label=u'TX')

        # Fill rx.
        plt.fill_between(x, data[u'f1'], 0, color=u'green', alpha='0.6')
        plt.fill_between(x, data[u'f2'], 0, color=u'blue', alpha='0.4')
        


    #plt.title(task[u'title'])
    plt.title(titleis)
    plt.grid(True)
    plt.legend(loc=u'upper left', shadow=True)

    plt.xlabel(u'[%d] : minuts' % minuts)
    plt.ylabel(ylabelis)

    plt.savefig(save_destination, dpi=70)

    plt.close()

    tools.log.debug(u'Drawing data for [%s] to (%s)\n', task[u'title'], save_destination)
