set datafile separator ","

set lmargin at screen 0.25
set rmargin at screen 0.8
set bmargin at screen 0.3
set tmargin at screen 0.8

set xlabel "Spreading Factor (SF)" rotate by 306 offset 5,-0.1 font "Arial,11.5"
set ylabel "Regional configuration" rotate by 0 offset -2,-0.3 font "Arial,11.5"
set zlabel "Collision rate (%)" rotate by 90  offset 1,0 font "Arial,11.5"

set xrange [6.5:12.5]
set yrange [0.5:4.5]
set zrange [0:7.5]

set xtics 1 font "Arial,10"
set ytics ("CN470" 1, "AS915" 2, "EU868" 3, "EU433" 4) font "Arial,10"
set ztics font "Arial,11"

set grid
set view 50,250
set xyplane at 0

set boxwidth 0.5
set boxdepth 0.47
set style fill solid 0.6 border lc rgb "0x555555"

set key at screen 1, 0.87 left top
set key spacing 0.8
set key samplen 0.8
set key width -18
set key font "Arial,10"

set label textcolor rgb "black"
set label "0.8" at 7,1.13,1.5 font "Arial,10.5" center front
set label "2.7" at 12,1.1,3.5 font "Arial,10.5" center front
set label "0.8" at 7,2.13,1.6 font "Arial,10.5" center front
set label "5.9" at 12,2.1,6.65 font "Arial,10.5" center front
set label "0.8" at 7,3.13,1.55 font "Arial,10.5" center front
set label "5.8" at 12,3.1,6.6 font "Arial,10.5" center front
set label "0.8" at 7,4.13,1.55 font "Arial,10.5" center front 
set label "5.7" at 12,4.1,6.55 font "Arial,10.5" center front

my_splot='splot \
    "average_collision_rate_by_region_by_sf.csv" every ::1 using 1:(4):4 with boxes lc rgb "0x4682B4" title "EU433", \
    "average_collision_rate_by_region_by_sf.csv" every ::1 using 1:(3):5 with boxes lc rgb "0xE69F00" title "EU868", \
    "average_collision_rate_by_region_by_sf.csv" every ::1 using 1:(2):2 with boxes lc rgb "0xCC3333" title "AS915", \
    "average_collision_rate_by_region_by_sf.csv" every ::1 using 1:(1):3 with boxes lc rgb "0x009E73" title "CN470"'

set terminal pdfcairo enhanced size 3.5, 2.8
set output "collision.pdf"
@my_splot

set terminal postscript eps enhanced color font "Arial,11" size 3.5, 2.8
set output "collision.eps"
@my_splot

set terminal svg enhanced size 350,280 font "Arial,11"
set output "collision.svg"
@my_splot