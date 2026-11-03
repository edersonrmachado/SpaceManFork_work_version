set datafile separator ","

set lmargin at screen 0.25
set rmargin at screen 0.8
set bmargin at screen 0.3
set tmargin at screen 0.8

set xlabel "Spreading Factor (SF)" rotate by 306 offset 5,-0.1 font "Arial,11.5"
set ylabel "EIRP (dBm)" rotate by 0 offset -2,-0.3 font "Arial,11.5"
set zlabel "Mean Link Margin Pass Rate (%)" rotate by 90  offset 1,0 font "Arial,11.5"

set xrange [6.5:12.5]
set yrange [0:32]
set zrange [0:100]

set xtics 1 font "Arial,10"
set ytics font "Arial,10"
set ztics font "Arial,11"

set grid
set view 50,250
set xyplane at 0

set boxwidth 0.5
set boxdepth 0.47
set style fill solid 0.6 border lc rgb "0x555555"

set key at screen 1, 0.84 left top
set key spacing 0.8
set key samplen 0.8
set key width -18
set key font "Arial,10"

# Mapeamento das colunas baseado na ordem alfabética do unstack do Pandas:
# Coluna 1: sf | Coluna 2: eirp_dbm | Coluna 3: AS915 | Coluna 4: CN470 | Coluna 5: EU433 | Coluna 6: EU868
my_splot='splot \
    "average_link_margin_pass_rate_by_region_sf_eirp.csv" every ::1 using 1:2:5 with boxes lc rgb "0x4682B4" title "EU433", \
    "average_link_margin_pass_rate_by_region_sf_eirp.csv" every ::1 using 1:2:($5 > 1 ? $5 + 9 : 1/0):(sprintf("%.1f", $5)) with labels font "Arial,10.5" textcolor rgb "black" notitle, \
    \
    "average_link_margin_pass_rate_by_region_sf_eirp.csv" every ::1 using 1:2:6 with boxes lc rgb "0xE69F00" title "EU868", \
    "average_link_margin_pass_rate_by_region_sf_eirp.csv" every ::1 using 1:2:($6 > 1.5 ? $6 + 10 : 1/0):(sprintf("%.1f", $6)) with labels font "Arial,10.5" textcolor rgb "black" notitle, \
    \
    "average_link_margin_pass_rate_by_region_sf_eirp.csv" every ::1 using 1:2:3 with boxes lc rgb "0xCC3333" title "AS915", \
    "average_link_margin_pass_rate_by_region_sf_eirp.csv" every ::1 using 1:2:($3 > 1 ? $3 + 10 : 1/0):(sprintf("%.1f", $3)) with labels font "Arial,10.5" textcolor rgb "black" notitle, \
    \
    "average_link_margin_pass_rate_by_region_sf_eirp.csv" every ::1 using 1:2:4 with boxes lc rgb "0x009E73" title "CN470", \
    "average_link_margin_pass_rate_by_region_sf_eirp.csv" every ::1 using 1:($2 + 0):($4 > 1 ? $4 + 5 : 1/0):(sprintf("%.1f", $4)) with labels font "Arial,10.5" textcolor rgb "black" notitle'

set terminal pdfcairo enhanced size 3.5, 2.8
set output "link_pass_3d.pdf"
@my_splot

set terminal postscript eps enhanced color font "Arial,11" size 3.5, 2.8
set output "link_pass_3d.eps"
@my_splot

set terminal svg enhanced size 350,280 font "Arial,11"
set output "link_pass_3d.svg"
@my_splot