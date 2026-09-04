import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


# files to evaluate
files=[
"../data/bw125_ldro0_f433_plen35_pped100_txp1.csv",
"../data/bw125_ldro0_f433_plen51_pped100_txp1.csv",
"../data/bw125_ldro0_f433_plen100_pped100_txp1.csv",
"../data/bw125_ldro0_f433_plen200_pped100_txp1.csv"
]

# save the plots on `image_folder` if true
SAVE_PLOTS=True
image_folder="../figures/"

# output filenames (freq_bw)
fig_1='pdr433_125a.pdf'
fig_2="energy433_125a.pdf"

# plots this limits must be customized according of max graph values
y_sup_lim=44.99 # PDR plot
y_sup_lim_2=24000 # energy plot

# general plot config
fig_facecolor='#FFFFFF'
dpi_set=600
fig_width=3.5*2.5
fig_height=2.2*4 
fontsize_xyticks=10 
fontsize_labels=12
fontsize_legend=12
width = 0.15
gap = 0.02
y_inf_lim=0
vis_pkt_color="slategray"
collided_pkt_color="orange"
dop_error_pkt_color="brown"
suc_rec_pkt_color="olivedrab"
box_width = 0.08
box_height = 0.22
box_gap=0.01
bar_lab_fontsize=12
y_ticks_fontsize=12
fontsize_info=12
box_color="whitesmoke"

# first plot PDR 
fig,ax=plt.subplots( nrows=len(files),ncols=1,figsize=(fig_width, fig_height),dpi=dpi_set,facecolor=fig_facecolor, gridspec_kw={'hspace':0.0}) 
ax = np.atleast_1d(ax)

for i, file in enumerate(files):
    
    df = pd.read_csv(file)
    
    non_visible_pkt_pct=100*df["non_visible"]/df["total_pkt"]
    visible_pkt_pct= 100*(df["total_pkt"]-df["collided"]-df["non_visible"])/df["total_pkt"]
    link_margin_pkt_pct=100*((df["link_margin_energy_pass"]/df["pkt_energy"]) /df["total_pkt"])
    collided_pkt_pct=100*df["collided"]/df["total_pkt"]
    doppler_error_pkt_pct=100*df["doppler_error"]/df["total_pkt"]
    success_rec_tx=100*df["succes_rec_tx"]/df["total_pkt"]


    x = np.arange(len(df["sf"]))
    
    bars_collided=ax[i].bar(x - 1.5*(width+gap), collided_pkt_pct, width,
                        color=collided_pkt_color, label="Collided")
    bars_visible=ax[i].bar(x - 0.5*(width+gap), visible_pkt_pct, width,
                       color=vis_pkt_color, label="Visible")
    bars_doppler=ax[i].bar(x + 0.5*(width+gap), doppler_error_pkt_pct, width,
                       color=dop_error_pkt_color, label="Doppler error")
    bars_link_margin=ax[i].bar(x + 1.5*(width+gap), link_margin_pkt_pct, width,
                        color="lightcoral", label="Link Margin")
    bars_received=ax[i].bar(x + 2.5*(width+gap), success_rec_tx, width,
                        color=suc_rec_pkt_color, label="Received/PDR")
    
    for pos in range(len(x)-1):
        ax[i].axvline(pos + 0.5, color="black", linestyle="--", linewidth=0.6,alpha=1)    

    if i == 0:
        n_sf = len(df["sf"])
        for j, sf in enumerate(df["sf"]):
            rect = Rectangle( (j - 0.5, 1 + box_gap*3),1,box_height,transform=ax[0].get_xaxis_transform(),facecolor=box_color,edgecolor="black",linewidth=1,clip_on=False)
            ax[0].add_patch(rect)
            ax[0].text((j + 0.5) / n_sf,1 + box_gap + box_height/2,str(sf),transform=ax[0].transAxes,ha="center",va="center",fontsize=12,fontweight="bold",clip_on=False)
                
    ax[i].set_ylabel("% of Total",fontsize=fontsize_labels)
    ax[i].set_ylim([y_inf_lim, y_sup_lim])
    ax[i].tick_params(axis="y", labelsize=y_ticks_fontsize)
    ax[i].grid(axis="y", alpha=0.2)
    ax[i].set_xticks([])
    ax[i].yaxis.tick_right()
    ax[i].yaxis.set_label_position("right")
    ax[i].tick_params(axis="y",left=False,right=True, labelleft=False, labelright=True)

    rect = Rectangle((-box_gap - box_width, 0), box_width, 1.0, transform=ax[i].transAxes, facecolor=box_color, edgecolor="black",
 linewidth=1, clip_on=False)
    ax[i].add_patch(rect)
    ax[i].text( -box_gap - box_width/2, 0.5, df["pkt_len"][0], transform=ax[i].transAxes, ha="center", va="center", fontsize=12, fontweight="bold",clip_on=False               
    )
    
    ax[i].bar_label(bars_collided, fmt="%.0f", padding=2, fontsize=bar_lab_fontsize)
    ax[i].bar_label(bars_visible, fmt="%.0f", padding=2, fontsize=bar_lab_fontsize)
    ax[i].bar_label(bars_doppler, fmt="%.0f", padding=2, fontsize=bar_lab_fontsize)
    ax[i].bar_label(bars_link_margin, fmt="%.0f", padding=2, fontsize=bar_lab_fontsize)                     
    ax[i].bar_label(bars_received, fmt="%.0f", padding=2, fontsize=bar_lab_fontsize)
        
handles, labels = ax[0].get_legend_handles_labels()
fig.legend( handles, labels, loc="upper center", ncol=4, bbox_to_anchor=(0.53, 1.05), fontsize=fontsize_legend, frameon=False)

box_x = -0.093
box_y = 1.03
box_w = 0.08
box_h = 0.18

ax[0].plot([box_x, box_x + box_w], [box_y + box_h, box_y], transform=ax[0].transAxes, color="black", linewidth=1, clip_on=False)
ax[0].text( box_x + box_w*0.73, box_y + box_h*0.5+0.05, "SF", transform=ax[0].transAxes, ha="center", va="center", fontsize=13, fontweight="bold", clip_on=False)
ax[0].text(box_x + box_w*0.25+0.01, box_y + box_h*0.5-0.05, "L", transform=ax[0].transAxes, ha="center", va="center", fontsize=13,fontweight="bold", clip_on=False)

df_info = pd.read_csv(files[0])

freq = df_info["freqMHz"][0]
bw = df_info["bw"][0]
ldro = df_info["ldro"][0]

if ldro == 0:
    ldro_text = "OFF"
else:
    ldro_text = str(ldro)

fig.text(0.5, -0.02, f"Frequency={freq:.0f} MHz   LDRO={ldro_text}   B={bw:.2f} kHz", ha="center", va="center", fontsize=fontsize_info)

# save option
if SAVE_PLOTS:
    fig.tight_layout()
    plt.savefig(image_folder+fig_1,bbox_inches='tight') 

# plt.show()


# plot Energy 

# general plot config
width = 0.17
gap = 0.06
bar_lab_fontsize=10
fig2,ax=plt.subplots( nrows=len(files),ncols=1,figsize=(fig_width, fig_height),dpi=dpi_set,facecolor=fig_facecolor, gridspec_kw={'hspace':0.0}) 
ax = np.atleast_1d(ax)

for i, file in enumerate(files):
    
    df = pd.read_csv(file)
    
    total_energy=df["total_energy"]
    visible_pkt_pct= (df["total_pkt"]-df["collided"]-df["non_visible"])
    visible_energy=visible_pkt_pct*df["pkt_energy"]
    failed_energy_col_=df["failed_energy_col"]
    failed_energy_dop=df["failed_energy_dop"]
    succes_energy_trans=df["succes_energy_trans"]

    x = np.arange(len(df["sf"]))
    bars_collided=ax[i].bar(x - 1.5*(width+gap), failed_energy_col_, width,
                        color=collided_pkt_color, label="Collided")
    bars_visible=ax[i].bar(x - 0.5*(width+gap), visible_energy, width,
                       color=vis_pkt_color, label="Visible")
    bars_doppler=ax[i].bar(x + 0.5*(width+gap), failed_energy_dop, width,
                       color=dop_error_pkt_color, label="Doppler error")
    bars_received=ax[i].bar(x + 1.5*(width+gap),succes_energy_trans, width,
                        color=suc_rec_pkt_color, label="succes. trans.")
    
    for pos in range(len(x)-1):
        ax[i].axvline(pos + 0.5, color="black", linestyle="--", linewidth=0.6,alpha=1)    

    if i == 0:
        n_sf = len(df["sf"])
        for j, sf in enumerate(df["sf"]):
            rect = Rectangle( (j - 0.5, 1 + box_gap*3),1,box_height,transform=ax[0].get_xaxis_transform(),facecolor=box_color,edgecolor="black",linewidth=1,clip_on=False)
            ax[0].add_patch(rect)
            ax[0].text((j + 0.5) / n_sf,1 + box_gap + box_height/2,str(sf),transform=ax[0].transAxes,ha="center",va="center",fontsize=12,fontweight="bold",clip_on=False)
                
    ax[i].set_ylabel("Energy (Joules)",fontsize=fontsize_labels)
    ax[i].set_ylim([y_inf_lim, y_sup_lim_2])
    ax[i].tick_params(axis="y", labelsize=y_ticks_fontsize)
    ax[i].grid(axis="y", alpha=0.2)
    ax[i].set_xticks([])
    ax[i].yaxis.tick_right()
    ax[i].yaxis.set_label_position("right")
    ax[i].tick_params(axis="y",left=False,right=True, labelleft=False, labelright=True)

    rect = Rectangle((-box_gap - box_width, 0), box_width, 1.0, transform=ax[i].transAxes, facecolor=box_color, edgecolor="black",
 linewidth=1, clip_on=False)
    ax[i].add_patch(rect)
    ax[i].text( -box_gap - box_width/2, 0.5, df["pkt_len"][0], transform=ax[i].transAxes, ha="center", va="center", fontsize=12, fontweight="bold",clip_on=False)
    
    ax[i].bar_label(bars_collided, fmt="%.0f", padding=2, fontsize=bar_lab_fontsize, rotation=90)
    ax[i].bar_label(bars_visible, fmt="%.0f", padding=2, fontsize=bar_lab_fontsize, rotation=90)
    ax[i].bar_label(bars_doppler, fmt="%.0f", padding=2, fontsize=bar_lab_fontsize, rotation=90)
    ax[i].bar_label(bars_received, fmt="%.0f", padding=2, fontsize=bar_lab_fontsize, rotation=90)
        
handles, labels = ax[0].get_legend_handles_labels()
fig2.legend( handles, labels, loc="upper center", ncol=4, bbox_to_anchor=(0.53, 0.99), fontsize=fontsize_legend, frameon=False)

box_x = -0.093
box_y = 1.03
box_w = 0.08
box_h = 0.18

ax[0].plot([box_x, box_x + box_w], [box_y + box_h, box_y], transform=ax[0].transAxes, color="black", linewidth=1, clip_on=False)
ax[0].text( box_x + box_w*0.73, box_y + box_h*0.5+0.05, "SF", transform=ax[0].transAxes, ha="center", va="center", fontsize=13, fontweight="bold", clip_on=False)
ax[0].text(box_x + box_w*0.25+0.01, box_y + box_h*0.5-0.05, "L", transform=ax[0].transAxes, ha="center", va="center", fontsize=13,fontweight="bold", clip_on=False)


df_info = pd.read_csv(files[0])

freq = df_info["freqMHz"][0]
bw = df_info["bw"][0]
ldro = df_info["ldro"][0]
tx_power=df["tx_power"][0]
if ldro == 0:
    ldro_text = "OFF"
else:
    ldro_text = str(ldro)

fig2.text(0.5, +0.06, f"Frequency={freq:.0f} MHz   LDRO={ldro_text}   B={bw:.2f} kHz   Tx power={tx_power} W", ha="center", va="center" , fontsize=fontsize_info)

# save option
if SAVE_PLOTS:
    fig.tight_layout()
    plt.savefig(image_folder+fig_2,bbox_inches='tight') 
# plt.show()