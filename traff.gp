#
# Traffic graph.
#

set terminal pngcairo size 600,300 enhanced font 'Verdana,10'

set output '/tmp/graphs/traff_wlp1s0.png'
data_file = '/tmp/gnuplot/traff_wlp1s0.txt'

set grid
set title   'Wifi Traffic'
set ylabel  'Mbytes'
set xlabel  '7 Hours'
set border linewidth 2

unset xtics

plot    data_file using 0:1 title 'RX' with lines,     \
        data_file using 0:2 title 'TX' with lines 
