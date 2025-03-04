from collections import Counter
from typing import Optional

import numpy as np
from matplotlib import pyplot as plt


def plot_side_by_side_histograms(
        data1: np.ndarray,
        data2: np.ndarray,
        labels: tuple = ("Dataset 1", "Dataset 2"),
        colors: tuple = ("blue", "orange"),
        normalize=False,
        title: Optional[str] =None
) -> None:
    """
    Plots two histograms side-by-side for each bin.

    :param data1: First dataset as a numpy array.
    :param data2: Second dataset as a numpy array.
    :param bins: Number of bins for the histograms.
    :param labels: Tuple containing labels for the datasets.
    :param colors: Tuple containing colors for the datasets.
    """
    # Compute the histogram bins and edges

    # todo: can either specify num_bins or actual bins
    # bins = np.arange(0, num_bins)
    bins='auto'

    hist1, bin_edges = np.histogram(data1, bins=bins)
    hist2, _ = np.histogram(data2, bins=bin_edges)

    # normalize
    if normalize:
        hist1 = hist1/hist1.sum()
        hist2 = hist2/hist2.sum()

    # Width of each bar
    bar_width = (bin_edges[1] - bin_edges[0]) / 3

    # Bin positions for each dataset
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    positions1 = bin_centers - bar_width / 2
    positions2 = bin_centers + bar_width / 2    # Plot the histograms

    plt.figure(figsize=(8, 6))
    plt.bar(positions1, hist1, width=bar_width, label=labels[0], color=colors[0], alpha=0.7)
    plt.bar(positions2, hist2, width=bar_width, label=labels[1], color=colors[1], alpha=0.7)

    # Add labels, legend, and grid
    plt.xlabel("Bins")
    plt.ylabel("Frequency")
    if title:
        plt.title(title)
    plt.xticks(ticks=bin_centers, labels=[f"{v:.2f}" for v in bin_centers], rotation=45)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()


def plot_histogram_from_counter(counter: Counter, bin_size: int) -> None:
    """
    Plot a histogram from a Counter object with specified bin sizes.

    Args:
        counter (Counter): Counter object containing data counts.
        bin_size (int): Size of each bin.
    """
    # Extract values and their frequencies from the counter
    values, frequencies = zip(*counter.items())

    # Flatten the data based on frequencies for histogram plotting
    data: List[int] = []
    for value, freq in counter.items():
        data.extend([value] * freq)

    # Plot the histogram
    # plt.hist(data, bins=range(min(data), max(data) + bin_size, bin_size), edgecolor='black', align='left')
    plt.hist(data, bins=range(min(data), 100 + bin_size, bin_size),
             edgecolor='black', align='left')
    plt.title("Histogram from Counter")
    plt.xlabel("Values")
    plt.ylabel("Frequency")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
