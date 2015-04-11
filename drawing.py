from tools import show_info

import matplotlib
matplotlib.use(u'Agg')

import matplotlib.pyplot as plt
import os.path
import config

def draw_data(data, task, minuts):
    save_destination = os.path.join(config.workdir, task[u'graph_file'])

    if __debug__: show_info((u'Draw data for', task[u'title']), u'\t', ending=u'to ' + u'[' + save_destination + u']')

    x = [ t for t in range(minuts) ]

    if task[u'title'] == u'cpu_temp':
        ylabelis = u'Temperature C'
        plt.plot(x, data, u'k', label=u'Temperature')
        plt.fill_between(x, data, 0, color=u'red', alpha='0.8')

    elif task[u'title'] == u'load_average':
        ylabelis = u'Load Average'
        plt.plot(x, data[0], u'r', label=u'1 minut')
        plt.plot(x, data[1], u'b', label=u'5 minuts')
        plt.plot(x, data[2], u'g', label=u'15 minuts')
            

    plt.title(task[u'title'])
    plt.grid(True)
    plt.legend(loc=u'upper left', shadow=True)

    plt.xlabel(u'time')
    plt.ylabel(ylabelis)

    plt.savefig(save_destination, dpi=70)

    plt.close()
