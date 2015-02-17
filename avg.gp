#
# Load average graph.
#

set terminal pngcairo size 600,300 enhanced font 'Verdana,10'

set output '/tmp/graphs/avg.png'
data_file = '/tmp/gnuplot/avg_data.txt'

set grid
set title 'Load Average Graphic'
set ylabel 'Load Average'
set xlabel '7 Hours'
set border linewidth 2

unset xtics

plot data_file using 0:1 title '1 minut' with lines,    \
     data_file using 0:2 title '5 minuts' with lines,   \
     data_file using 0:3 title '15 minuts' with lines
