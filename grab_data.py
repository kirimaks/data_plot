import time

# System files.
cpu_temp_file = open('/sys/class/hwmon/hwmon0/temp1_input')
load_avg_file = open('/proc/loadavg')

# Data files.
cpu_temp_out_file = '/tmp/gnuplot/temp_data.txt'
load_avg_out_file = '/tmp/gnuplot/avg_data.txt'

global_delay = 10
max_data_entries = 2500 

def truncate_file(file_to_truncate):
    fl = open(file_to_truncate)
    cur_lines = fl.readlines()
    fl.close()

    fl = open(file_to_truncate, 'w')
    for line in cur_lines[1:-1]:
        fl.write(line)

    fl.close()


while True:
    ########################
    #### Cpu temperature ###
    ########################
    cpu_temp_out = open(cpu_temp_out_file, 'a')
    cur_temp = cpu_temp_file.read()[:2]     # Read current temperature.
    cpu_temp_file.seek(0)                   # Rewind file.
    cpu_temp_out.write(cur_temp + '\n')     # Write current temperature.
    cpu_temp_out.close()

    lines_in_file = sum(1 for l in open(cpu_temp_out_file))

    if lines_in_file >= max_data_entries:   
        truncate_file(cpu_temp_out_file)
    
    ####################
    ### Load average ###
    ####################
    load_avg_out = open(load_avg_out_file, 'a')
    cur_avg = load_avg_file.read()
    load_avg_file.seek(0)
    load_avg_out.write(cur_avg[:14] + '\n')
    load_avg_out.close() # Flush.

    lines_in_file = sum(1 for l in open(load_avg_out_file))
    if lines_in_file >= max_data_entries:
        truncate_file(load_avg_out_file)

    ########################
    ### Cpu usage by top ###
    ########################

    ########################
    ### Traffic (mbytes) ###
    ########################

    time.sleep(global_delay)  # Global delay.
