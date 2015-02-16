#
# Load average graph.
#

set terminal pngcairo size 600,300 enhanced font 'Verdana,10'
set output '/tmp/graphs/avg.png'

set grid
set title 'Load Average Graphic'
set ylabel 'Load Average'
set xlabel '7 Hours'
set border linewidth 2

#set key off
unset xtics

#plot 'temp_data.txt' with filledcurve x1 lt rgb "#FF8C00"

plot    '/tmp/gnuplot/avg_data.txt' using 0:1 title '1 minut' with lines,   \
        '/tmp/gnuplot/avg_data.txt' using 0:2 title '5 minuts' with lines,   \
        '/tmp/gnuplot/avg_data.txt' using 0:3 title '15 minuts' with lines
