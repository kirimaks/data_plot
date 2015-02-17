import time

# System files.
cpu_temp_file = open('/sys/class/hwmon/hwmon0/temp1_input')
load_avg_file = open('/proc/loadavg')

# Working directory.
work_dir = '/tmp/gnuplot/'

# Data files.
cpu_temp_out_file = work_dir + 'temp_data.txt'
load_avg_out_file = work_dir + 'avg_data.txt'

global_delay = 2
max_data_entries = 2500 

def truncate_file(file_to_truncate):
    lines_in_file = sum(1 for l in open(load_avg_out_file))

    if lines_in_file < max_data_entries:
        return

    fl = open(file_to_truncate)
    cur_lines = fl.readlines()
    fl.close()

    fl = open(file_to_truncate, 'w')
    for line in cur_lines[1:-1]:
        fl.write(line)

    fl.close()


def get_cur_traffic(iface):
    rx_file = '/sys/class/net/' + iface + '/statistics/rx_bytes'
    tx_file = '/sys/class/net/' + iface + '/statistics/tx_bytes'
    traffic_out_file = work_dir + 'traff_' + iface + '.txt'

    r1 = open(rx_file).readline()
    t1 = open(tx_file).readline()
    time.sleep(1)
    r2 = open(rx_file).readline()
    t2 = open(tx_file).readline()

    cur_rx = str((int(r2)-int(r1))/1024)
    cur_tx = str((int(t2)-int(t1))/1024)

    traffic_out = open(traffic_out_file, 'a')
    traffic_out.write(cur_rx + '\t')
    traffic_out.write(cur_tx + '\n')
    traffic_out.close()

    truncate_file(traffic_out_file)


while True:
    ########################
    #### Cpu temperature ###
    ########################
    cpu_temp_out = open(cpu_temp_out_file, 'a')
    cur_temp = cpu_temp_file.read()[:2]     # Read current temperature.
    cpu_temp_file.seek(0)                   # Rewind file.
    cpu_temp_out.write(cur_temp + '\n')     # Write current temperature.
    cpu_temp_out.close()

    #lines_in_file = sum(1 for l in open(cpu_temp_out_file))
    #if lines_in_file >= max_data_entries:   
    #    truncate_file(cpu_temp_out_file)
    truncate_file(cpu_temp_out_file)
    
    ####################
    ### Load average ###
    ####################
    load_avg_out = open(load_avg_out_file, 'a')
    cur_avg = load_avg_file.read()
    load_avg_file.seek(0)
    load_avg_out.write(cur_avg[:14] + '\n')
    load_avg_out.close() # Flush.

    #lines_in_file = sum(1 for l in open(load_avg_out_file))
    #if lines_in_file >= max_data_entries:
    #    truncate_file(load_avg_out_file)
    truncate_file(load_avg_out_file)

    ########################
    ### Cpu usage by top ###
    ########################

    ########################
    ### Traffic (mbytes) ###
    ########################

    #get_cur_traffic('eth0')
    get_cur_traffic('wlp1s0')


    ####
    time.sleep(global_delay)  # Global delay.
