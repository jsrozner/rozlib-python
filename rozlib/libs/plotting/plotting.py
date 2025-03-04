import matplotlib.colors as mcolors

import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional

from matplotlib import patches
from matplotlib.figure import Figure
from sklearn.metrics import roc_curve, auc


# Example data
def plot_roc(
        labels,
        scores,
        show_thresholds = False,
        flip_threshold_sign=False,
        title=None,
        add_axes_labels=True,
        figsize=(5,5)
) -> Optional[Figure]:
    fpr, tpr, thresholds = roc_curve(labels, scores)

    # Step 3: Compute AUC (Area Under the Curve)
    roc_auc = auc(fpr, tpr)

    # Step 4: Plot the ROC curve
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(fpr, tpr, label=f"ROC (AUC = {roc_auc:.2f})", color='black')
    # plt.plot([0, 1], [0, 1], "k--", label="Random Guess")
    if add_axes_labels:
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
    for spine in ax.spines.values():
        spine.set_edgecolor('black')  # Set dark color (or 'white' for light mode)
    if title:
        ax.set_title(title)

    # ax.grid(True)
    tick_positions = np.arange(0, 1.1, 0.2)
    ax.set_xticks(tick_positions)
    ax.set_yticks(tick_positions)
    ax.tick_params(axis="both", which="both")
    # ax.minorticks_on()

    # Add threshold labels to the curve
    if show_thresholds:
        for i, threshold in enumerate(thresholds):
            if i == 0: continue
            if i % 2000 != 0:
                continue # avoid clutter

            thres_x_label_shift = 0.02
            if i < 10000:
                thres_y_label_shift = 0
            else:
                thres_y_label_shift = -0.02

            thres = threshold if not flip_threshold_sign else -threshold
            plt.text(fpr[i]+thres_x_label_shift, tpr[i]+thres_y_label_shift, f"{thres:.2f}", fontsize=10, color="black")

    ax.legend(loc="lower right", frameon=False)
    # ax.show()
    return fig

def add_rect_to_grid(
        ax: matplotlib.axes.Axes,
        num_segments: int,
        x_start: int,
        y_start: int,
        x_len_incs: int,
        y_len_incs: int,
        color,
        linewidth=2
):
    y_limits = ax.get_ylim()
    x_limits = ax.get_xlim()
    # print(y_limits)
    # print(x_limits)
    x_size = x_limits[1] - x_limits[0]
    y_size = y_limits[1] - y_limits[0]
    inc_x = x_size/num_segments
    inc_y = y_size/num_segments

    x = x_limits[0] + x_start * inc_x
    y = y_limits[0] + y_start * inc_y

    rect = patches.Rectangle((x, y),
                             width=x_len_incs * inc_x,
                             height=y_len_incs * inc_y,
                             linewidth=linewidth,
                             edgecolor=color,
                             facecolor='none')
    ax.add_patch(rect)

def add_X_to_plot(
        ax: matplotlib.axes.Axes,
        num_segments_x: int,
        num_segments_y: int,
        x_start: int,
        y_start: int,
        color = "k",
        linewidth=1,
        do_print=False
):
    y_limits = ax.get_ylim()
    x_limits = ax.get_xlim()
    x_size = x_limits[1] - x_limits[0]
    # todo: why flipped
    y_size = y_limits[1] - y_limits[0]
    inc_x = x_size/num_segments_x
    inc_y = y_size/num_segments_y

    x = x_limits[0] + x_start * inc_x
    y = y_limits[0] + y_start * inc_y

    if do_print:
        print(f"Add X to plot {num_segments_x}, {num_segments_y} {x_start}, {y_start}")
        print(x_limits, y_limits)
        print(x_size, y_size)
        print(inc_x, inc_y)
        print(x,y)

    ax.plot((x,x+inc_x), (y, y+inc_y), linewidth=linewidth, color=color)
    ax.plot((x,x+inc_x), (y+inc_y, y), linewidth=linewidth, color=color)


def print_color_map_with_hex(cmap):
    # Extract colors from the colormap
    num_colors = cmap.N  # Number of colors in the colormap
    colors = [cmap(i) for i in range(num_colors)]  # Get RGBA values

    # Convert to HEX
    hex_colors = [mcolors.to_hex(c) for c in colors]
    hex_colors = [h.strip("#") for h in hex_colors]

    # Plot colors with hex codes
    fig, ax = plt.subplots(figsize=(8, 2))

    for i, (hex_color, rgba) in enumerate(zip(hex_colors, colors)):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=rgba))
        ax.text(i + 0.5, -0.2, hex_color, ha="center", fontsize=10)

    ax.set_xlim(0, num_colors)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Dark2 Colormap with HEX Codes", fontsize=12)

    # return fig


