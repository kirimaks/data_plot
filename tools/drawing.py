import matplotlib.pyplot as plt
import os.path

class Drawing(object):
    ''' Super class for all another drawing classes. '''
    
    def __init__(self, task_name, data, conf, log_tool, minuts):
        self.__log_tool    = log_tool
        self.__task_name   = task_name
        self.__data        = data
        self.__output_file = os.path.join(conf.get(u'Basic', u'workdir'), conf.get(task_name, u'graph_file'))
        self.__minuts      = minuts

        if int(self.__minuts) <= 5:
            self.__log_tool.crit([u'Too few minutes. Exit.....'])

        
    def create_graph(self):
        self.__log_tool.debug( [u'Write data for [%s] to [%s]', self.__task_name, self.__output_file] )
    
        ### Adjust time. ###
        if len(self.__data[u'Time']) < self.__minuts:
            self.__minuts = len(self.__data[u'Time'])

        ### Create x points.  ###
        x_points = [ t for t in range(self.__minuts) ]

        ### Prepare time. ###
        time = self.prepare_time(self.__data[u'Time'])

        ax = plt.gca()
        time_range = range(-1, self.__minuts, self.__minuts/4)
        time_range[0] = 0
        ax.set_xticks(time_range)
        ax.set_xticklabels(time)

        #------ Colors. -----------------------------------------------
        colors_list = [ u'b', u'g', u'r', u'c', u'm', u'y', u'k' ]
        #--------------------------------------------------------------

        #---- Add every array with data. -------
        for k in self.__data.keys():

            #--- Generage random color. ----------------------------------------
            import random
            cur_color = colors_list[ random.randrange(0, len(colors_list)-1) ]
            #-------------------------------------------------------------------

            if k != u'Time':
                plt.plot(x_points, self.__data[k], cur_color, label=k)
        #---------------------------------------


        plt.title(self.__task_name)
        plt.grid(True)
        plt.legend(loc=u'upper left', shadow=True)
        plt.xlabel(u'[%d] : minuts' % self.__minuts)

        plt.savefig( self.__output_file, dpi=70 )
        plt.close()



    def prepare_time(self, t):
        time = []

        first_elem = 0
        last_elem = len(t)-1
        mid_elem = last_elem/2
        first_part = mid_elem/2
        last_part = mid_elem + first_part

        time.append(t[first_elem])
        time.append(t[first_part])
        time.append(t[mid_elem])
        time.append(t[last_part])
        time.append(t[last_elem])

        return time


        
