#
# Temperature graph.
#

set terminal pngcairo size 600,300 enhanced font 'Verdana,10'
set output '/tmp/graphs/temp.png'

set grid
set title 'Temperature Graphic'
set ylabel 'C Temp'
set xlabel '7 Hours'
set border linewidth 2

set key off
unset xtics

plot '/tmp/gnuplot/temp_data.txt' with filledcurve x1 lt rgb "#FF8C00"
