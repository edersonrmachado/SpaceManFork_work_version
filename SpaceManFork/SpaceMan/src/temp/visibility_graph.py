import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

SAVE_PLOTS=True

num_satellites=[5,10,15,20,25,50,75,100,125,150,175,200]
visible_tx=[265,464,628,849,950,1557,1824,1903,1933,1946,1954,1978]
visible_percentage=[13.34,23.63,31.62,42.75,52.17,78.4,91.84,95.82,97.33,97.99,98.39,99.70]
sim_time=[19.27,81.04,114.3,119.54,161.87,239.52, 990.73,411.95, 1093.67,1113.70,1121.14 ,766.41]




num_satellites = [5, 25, 50, 100, 200]

visible_tx = [265, 950, 1557, 1903, 1978]

visible_percentage = [13.34, 52.17, 78.4, 95.82, 99.70]

sim_time = [19.27, 161.87, 239.52, 411.95, 766.41]


num_satellites = [5, 25, 50, 75, 100, 125, 150, 175, 200]

visible_tx = [265, 950, 1557, 1824, 1903, 1933, 1946, 1954, 1978]

visible_percentage = [13.34, 52.17, 78.4, 91.84, 95.82, 97.33, 97.99, 98.39, 99.70]

sim_time = [19.27, 161.87, 239.52, 990.73, 411.95, 1093.67, 1113.70, 1121.14, 766.41]



image_folder='../../figures/'
# fig name
fig_1='simulation_time.pdf'
fig_2='visibility_bar_percentage.pdf'
fig_3='visibility_bar_transmissions.pdf'

# set plot  fonts
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

# plots - customized style
fig_facecolor='#FFFFFF'
dpi_set=700
fig_width=3.5
fig_height=2.2
fontsize_ticks=9
fontsize_leg=8
fontsize_xy_labels=10 
lwid_leg=1.5 
lwid_plots=1
markersize_plt=2
colorbars="navy"#'mediumblue'
fontsize_bars_labels=9
  
    # fig
fig1,ax1=plt.subplots(figsize=(fig_width, fig_height),dpi=dpi_set,facecolor=fig_facecolor) 

ax1.plot(num_satellites,sim_time, marker='o', color='blue', label='Visible Transmissions', linewidth=lwid_plots, markersize=markersize_plt)
ax1.set_xlabel('Number of Satellites', fontsize=fontsize_xy_labels)
ax1.set_ylabel('Simulation time (s)', fontsize=fontsize_xy_labels)
#ax1.set_xticks([5,25,50,100,200])
ax1.set_xticks(num_satellites)
ax1.set_yticks(sim_time + [1000] )
ax1.tick_params(axis='both', which='major', labelsize=fontsize_ticks)
ax1.tick_params(axis='x', labelrotation=0)
ax1.grid(
    True,
    linestyle='--',
    linewidth=0.5
)
#ax1.set_ylim([0, 1000])

ax1.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
# save option
if SAVE_PLOTS:
    plt.savefig(image_folder+fig_1,bbox_inches='tight') 
#plt.show()

'''
num_satellites = [5, 25, 50, 100, 200]

visible_tx = [265, 950, 1557, 1903, 1978]

visible_percentage = [13.34, 52.17, 78.4, 95.82, 99.70]

sim_time = [19.27, 161.87, 239.52, 411.95, 766.41]
'''
###################################################################

fig2,ax2=plt.subplots(figsize=(fig_width, fig_height),dpi=dpi_set,facecolor=fig_facecolor) 
# Gráfico de barras
bars = ax2.bar(
    num_satellites,
    visible_percentage,
    width=6,
    color=colorbars,
    label='Visible Transmissions'
)

ax2.bar_label(
    bars,
    padding=1,
    labels=[f'{v:.1f}' for v in visible_percentage],
    fontsize=fontsize_bars_labels
)

ax2.set_xlabel(
    'Number of Satellites',
    fontsize=fontsize_xy_labels
)

ax2.set_ylabel(
    'Visible Transmissions (%)',
    fontsize=fontsize_xy_labels
)

ax2.set_xticks(num_satellites)

ax2.set_yticks(visible_percentage + [100])

ax2.tick_params(
    axis='both',
    which='major',
    labelsize=fontsize_ticks
)

ax2.tick_params(
    axis='x',
    labelrotation=0
)

ax2.grid(
    True,
    axis='y',
    linestyle='--',
    alpha=0.5
)

ax2.set_yticks([0,100] )
ax2.set_ylim([0, 125])
# save option
if SAVE_PLOTS:
    plt.savefig(image_folder+fig_2,bbox_inches='tight') 

######################################### 

fig3,ax3=plt.subplots(figsize=(fig_width, fig_height),dpi=dpi_set,facecolor=fig_facecolor) 
# Gráfico de barras
bars = ax3.bar(
    num_satellites,
    visible_tx,
    width=5,
    color=colorbars,
    label='Visible Transmissions'
)

ax3.bar_label(
    bars,
    padding=0,
    fontsize=fontsize_ticks
)

ax3 .set_xlabel(
    'Number of Satellites',
    fontsize=fontsize_xy_labels
)

ax3.set_ylabel(
    'Visible Transmissions',
    fontsize=fontsize_xy_labels
)

ax3.set_xticks(num_satellites)

ax3.set_yticks(visible_tx + [2000])

ax3.tick_params(
    axis='both',
    which='major',
    labelsize=fontsize_ticks
)

ax3.tick_params(
    axis='x',
    labelrotation=0
)

ax3.grid(
    True,
    axis='y',
    linestyle='--',
    alpha=0.5
)

ax3.set_yticks([0,2000] )
ax3 .set_ylim([0, 2500])
# save option
if SAVE_PLOTS:
    plt.savefig(image_folder+fig_3,bbox_inches='tight') 

