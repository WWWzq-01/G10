# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import itertools

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from statsFiguresUtil import *
from figureUtils import *

marker_arr = ["s", "o", "x", "^"]
line_styles = ["-.", "--", ":", "-"]
# hatch_color = "#78756e"
hatch_color = "white"

color_arr = colors_dark6
# color_arr = colors_test
# plot font size options
plt.rc("font", size=11)
plt.rc("xtick", labelsize=18)
plt.rc("ytick", labelsize=18)
plt.rc("legend", fontsize=18)

plt.rc("hatch", color="white")
mpl.rcParams["axes.labelsize"] = 22
mpl.rcParams["hatch.linewidth"] = 1.8
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams.update({'font.size': 16})
mpl.rcParams.update({'font.family': 'serif'})

fig, (((ax0, ax1, ax2, ax3, ax4))) = plt.subplots(1, 5, figsize=(27, 10))
plt.subplots_adjust(top=0.3, bottom=0.01, hspace=0.53, wspace=0.25)
axs = (ax0, ax1, ax2, ax3, ax4)

models = [RESNET, INCEPTION, BERT, VIT]
models = [RESNET, SENET, INCEPTION, VIT]
models = [BERT, VIT, INCEPTION, RESNET, SENET]
stat_prefix = "sensitivity_cpumem"
for model_idx in range(len(models)):
  ax = axs[model_idx]
  model = models[model_idx]
  if model == INCEPTION:
    data_file = f"{stat_prefix}/inception.txt"
  elif model == RESNET:
    data_file = f"{stat_prefix}/resnet.txt"
  elif model == SENET:
    data_file = f"{stat_prefix}/senet.txt"
  elif model == BERT:
    data_file = f"{stat_prefix}/bert.txt"
  elif model == VIT:
    data_file = f"{stat_prefix}/vit.txt"
  elif model == RESNEXT:
    data_file = f"{stat_prefix}/resnext.txt"

  bar_width = 0.105
  horiz_margin = 0.6
  horiz_major_tick = 0.7
  try:
    with open(data_file, "r") as f:
      lines = f.read()
  except Exception as e:
    continue

  first_dim_arr = []
  second_dim_arr = []
  sections = lines.strip().split("\n\n")
  first_dim_arr = [setting.strip() for setting in sections[0].split("|")]
  data_array = np.zeros((len(sections) - 1, len(first_dim_arr)))
  for section_idx, section in enumerate(sections[1:]):
    lines = section.strip().split("\n")
    second_dim = lines[0].strip()
    second_dim_arr.append(float(second_dim))
    data_array[section_idx, :] = np.array([float(data) for data in lines[1].split()]) / 1000
  for j, setting in enumerate(first_dim_arr):
    plot_idxs = data_array[:, j] != 0
    x_arr = [second_dim_arr[i] for i in range(len(plot_idxs)) if plot_idxs[i]]
    y_arr = [data_array[i, j] / 1200e3 for i in range(len(plot_idxs)) if plot_idxs[i]]
    ax.plot(x_arr, y_arr, linestyle=line_styles[j], color=color_arr[j], marker=marker_arr[j], markerfacecolor="none", label=first_dim_arr[j], linewidth=3, markersize=9)

  # ax.set_xticks(second_dim_arr)
  # ax.set_xticklabels([str(int(d)) for d in second_dim_arr])
  if model == RESNET:
    ax.set_xticks([0, 32, 64, 128, 192, 256])
  elif model == SENET:
    ax.set_xticks([0, 32, 64, 96, 128, 256])
  else:
    ax.set_xticks([0, 32, 64, 128, 256])
  ax.set_xlabel(f"Host Memory Capacity (GB)", fontsize=15)
  plt.text(0.5, -0.28, f"({chr(ord('a') + model_idx)}) {list(net_display_name_translation.values())[model]}", ha="center", transform=ax.transAxes)
  ax.legend(loc="upper right")
  ax.grid()
  ymin, ymax = ax.get_ylim()
  ytick = 10
  if model == INCEPTION:
    ymin, ymax, ytick = 45, 120, 15
  elif model == RESNET:
    ymin, ymax, ytick = 80, 330, 50
  elif model == SENET:
    ymin, ymax, ytick = 90, 340, 50
  elif model == BERT:
    ymin, ymax, ytick = 0, 70, 10
  elif model == VIT:
    ymin, ymax, ytick = 0, 25, 5
  yticks = range(ymin, ymax + 1, ytick)
  ax.set_ylim(ymin, yticks[-1])
  ax.set_yticks(yticks)
  
  # ax.set_ylim([0, (data_array[:, j]).max() * 1.2])
ax0.set_ylabel("Execution Time (sec)")

# handles, labels = ax.get_legend_handles_labels()
# print(labels)
# legend = fig.legend(handles, labels, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 0.375), ncols=6)

# shift = max([t.get_window_extent().width for t in legend.get_texts()])
# for t in legend.get_texts():
#     t.set_position(((shift - t.get_window_extent().width) / 2 - 6, 0))

plt.show()

extent = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).expanded(0.88, 0.85)
x_len, y_len = extent.x1 - extent.x0, extent.y1 - extent.y0
extent.y0 -= y_len * 0.178
extent.y1 -= y_len * 0.70
extent.x0 += x_len * 0.025
extent.x1 -= x_len * 0.035 
# figname = list(net_name_translation.values())[model]
# fig.savefig(f"OverallPerf{figname}.png", bbox_inches=extent)
fig.savefig(f"output/OverallPerfCPUMem.png", bbox_inches=extent)
fig.savefig(f"output/OverallPerfCPUMem.pdf", bbox_inches=extent)
