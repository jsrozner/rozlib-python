import os
import warnings
from pathlib import Path

import matplotlib
from matplotlib.figure import Figure


def save_fig(
        fig: Figure,
        figs_dir: Path,
        filename: str,
        transparent_bg = False
):
    """
    Will save a matplot Fig to filename

    Args:
        fig:
        filename:
        transparent_bg:

    Returns: None

    """
    # todo: add pdf if not already
    # todo: create fig dir if not existin
    if not os.path.isdir(figs_dir):
        raise Exception(f"{figs_dir} does not exist (cwd: {os.getcwd()}")

    # adjusted_fig = adjust_figure_height(fig, 3.2)
    fig.savefig(figs_dir / filename, bbox_inches="tight", pad_inches=.1, transparent=transparent_bg)


def config_matplot_for_latex(
        fontsize=12,
        legend_font_change=0,
        dpi=150
):
    """
    use fontsize = 14 for multiplot (3-plot, 3x3 figsize)
    and fontsize = 12 for single plots (1 plot, 5x3, usually)
    """
    warnings.warn(f"/Library/TeX/textbin will be added to path")
    os.environ["PATH"] += os.pathsep + "/Library/TeX/texbin"
    # font_size = 12
    matplotlib.rcParams.update({
        "text.usetex": True,  # Use LaTeX for rendering
        "font.family": "serif",
        "font.serif": ["Times"],  # Match LaTeX Times Roman font
        # "axes.labelsize": fontsize + 2,  # Match LaTeX font size
        "axes.labelsize": fontsize,  # Match LaTeX font size
        "xtick.labelsize": fontsize,
        "ytick.labelsize": fontsize -1,
        "legend.fontsize": fontsize + legend_font_change,
        "figure.dpi": dpi,
        "axes.edgecolor": "black"
    })

class FigSaver:
    """
    Tiny helper class to increment fig save count, so that figs can be saved without needing to name them.
    """
    def __init__(self, figs_dir: Path | str):
        print(f"Initializing fig saver at dir {figs_dir}")
        if not os.path.isdir(figs_dir):
            raise Exception(f"{figs_dir} does not exist")
        self.figs_dir = Path(figs_dir)
        self.ct = 0

    def save(self, fig, filename=None):
        # todo: check if path already exists or at least warn
        if filename is None:
            filename = f"f_{self.ct}.png"
        save_fig(fig, self.figs_dir, filename, transparent_bg=True)
        self.ct += 1
