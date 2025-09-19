import matplotlib.colors as mcolors

import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional, Iterable

from matplotlib import patches
from matplotlib.figure import Figure
from matplotlib.patches import PathPatch
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

def add_bottom_edge_to_grid(
    ax: matplotlib.axes.Axes,
    num_segments: int,
    x_start: int,
    y_start: int,
    x_len_incs: int,
    y_len_incs: int,
    color,
    linewidth: float = 2,
):
    y_limits = ax.get_ylim()
    x_limits = ax.get_xlim()

    x_size = x_limits[1] - x_limits[0]
    y_size = y_limits[1] - y_limits[0]

    inc_x = x_size / num_segments
    inc_y = y_size / num_segments

    # bottom-left corner
    x0 = x_limits[0] + x_start * inc_x
    y0 = y_limits[0] + y_start * inc_y
    # bottom-right corner
    x1 = x0 + x_len_incs * inc_x
    y1 = y0  # same y

    # Use a simple line segment as a patch
    line = patches.FancyArrowPatch(
        (x0, y0), (x1, y1),
        arrowstyle="-",        # plain line
        color=color,
        linewidth=linewidth,
        mutation_scale=0,      # no arrow head
    )
    ax.add_patch(line)

from matplotlib.path import Path



# def add_edges_to_grid(
#     ax: matplotlib.axes.Axes,
#     num_segments: int,
#     x_start: int,
#     y_start: int,
#     x_len_incs: int,
#     y_len_incs: int,
#     color: str | tuple[float, float, float] | tuple[float, float, float, float],
#     linewidth: float = 2.0,
#     sides: Iterable[str] = ("bottom", "left"),
# ) -> PathPatch:
#     """
#     Draw selected edges of the rectangle cell-block defined on a num_segments x num_segments grid.
#
#     sides: any of {"bottom", "top", "left", "right"}.
#            Default draws bottom and left.
#     """
#     y_limits = ax.get_ylim()
#     x_limits = ax.get_xlim()
#
#     x_size: float = float(x_limits[1] - x_limits[0])
#     y_size: float = float(y_limits[1] - y_limits[0])
#
#     inc_x: float = x_size / num_segments
#     inc_y: float = y_size / num_segments
#
#     # Corners of the target block in data coords
#     x0: float = x_limits[0] + x_start * inc_x
#     y0: float = y_limits[0] + y_start * inc_y
#     x1: float = x0 + x_len_incs * inc_x
#     y1: float = y0 + y_len_incs * inc_y
#
#     # Build a Path consisting of 0–4 independent line segments
#     verts: list[tuple[float, float]] = []
#     codes: list[int] = []
#
#     want = set(sides)
#
#     if "bottom" in want:
#         verts.extend([(x0, y0), (x1, y0)])
#         codes.extend([Path.MOVETO, Path.LINETO])
#
#     if "left" in want:
#         verts.extend([(x0, y0), (x0, y1)])
#         codes.extend([Path.MOVETO, Path.LINETO])
#
#     if "top" in want:
#         verts.extend([(x0, y1), (x1, y1)])
#         codes.extend([Path.MOVETO, Path.LINETO])
#
#     if "right" in want:
#         verts.extend([(x1, y0), (x1, y1)])
#         codes.extend([Path.MOVETO, Path.LINETO])
#
#     path = Path(verts, codes)
#     patch = PathPatch(path, fill=False, edgecolor=color, linewidth=linewidth, capstyle="butt")
#     ax.add_patch(patch)
#     return patch



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


def add_edges_to_grid(
    ax: matplotlib.axes.Axes,
    num_segments: int,
    x_start: int,
    y_start: int,
    x_len_incs: int,
    y_len_incs: int,
    color: str | tuple[float, float, float] | tuple[float, float, float, float],
    linewidth: float = 2.0,
    sides: Iterable[str] = ("bottom", "left"),
) -> PathPatch:
    x0, x1, y0, y1 = _rect_coords(ax, num_segments, x_start, y_start, x_len_incs, y_len_incs)

    # If bottom+left (or left+bottom), draw a single connected “L” to avoid a gap.
    s = set(sides)
    if s == {"bottom", "left"}:
        # Draw from bottom-right → bottom-left → top-left
        verts = [(x1, y0), (x0, y0), (x0, y1)]
        codes = [Path.MOVETO, Path.LINETO, Path.LINETO]
    else:
        # Fall back: independent segments (no shared join)
        verts, codes = [], []
        if "bottom" in s:
            verts += [(x0, y0), (x1, y0)]
            codes += [Path.MOVETO, Path.LINETO]
        if "left" in s:
            verts += [(x0, y0), (x0, y1)]
            codes += [Path.MOVETO, Path.LINETO]
        if "top" in s:
            verts += [(x0, y1), (x1, y1)]
            codes += [Path.MOVETO, Path.LINETO]
        if "right" in s:
            verts += [(x1, y0), (x1, y1)]
            codes += [Path.MOVETO, Path.LINETO]

    path = Path(verts, codes)
    patch = PathPatch(
        path,
        fill=False,
        edgecolor=color,
        linewidth=linewidth,
        capstyle="projecting",   # square ends
        joinstyle="miter",       # sharp corner
        antialiased=True,
        snap=False,              # set True if you prefer pixel snapping for raster backends
        zorder=10,
    )
    ax.add_patch(patch)
    return patch

def _rect_coords(
    ax: matplotlib.axes.Axes,
    num_segments: int,
    x_start: int,
    y_start: int,
    x_len_incs: int,
    y_len_incs: int,
) -> tuple[float, float, float, float]:
    (x_min, x_max) = ax.get_xlim()
    (y_min, y_max) = ax.get_ylim()
    inc_x = (x_max - x_min) / num_segments
    inc_y = (y_max - y_min) / num_segments
    x0 = x_min + x_start * inc_x
    y0 = y_min + y_start * inc_y
    x1 = x0 + x_len_incs * inc_x
    y1 = y0 + y_len_incs * inc_y
    return x0, x1, y0, y1



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


# Create colormap
def make_custom_cmap(colors: list[str], name: str):
    cmap = mcolors.LinearSegmentedColormap.from_list(name, colors)
    return cmap

# https://www.color-hex.com/color-palette/49436
ibm_colors = [
    "#ffb000",  # (255,176,0)
    "#fe6100",  # (254,97,0)
    "#dc267f",  # (220,38,127)
    "#785ef0",  # (120,94,240)
    "#648fff",  # (100,143,255)
]
def ibm_cmap():
    return make_custom_cmap(ibm_colors, "ibm")

ibm_colors2 = [
    "#D55E00", #	(213,94,0)
    "#CC79A7",#  	(204,121,167)
    "#0072B2",#  	(0,114,178)
    "#F0E442",#  	(240,228,66)
    "#009E73",#  	(0,158,115)
]

def ibm_cmap2():
    return make_custom_cmap(ibm_colors2, "ibm2")




