import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def normalize_to_frequency(values, total=5000):
    values = np.asarray(values, dtype=float)
    values = values / (values.sum() + 1e-12)
    return values * total


def plot_query_distribution_block(fig, outer_gs):
 

    rng = np.random.default_rng(7)
    num_queries = 30
    x = np.arange(1, num_queries + 1)

    baseline_epoch_0 = normalize_to_frequency(rng.gamma(0.7, 1.0, num_queries), 5000)
    baseline_epoch_10 = normalize_to_frequency(rng.gamma(0.6, 1.0, num_queries), 5000)
    baseline_epoch_25 = normalize_to_frequency(rng.gamma(0.55, 1.0, num_queries), 5000)

    ours_epoch_0 = normalize_to_frequency(rng.gamma(0.7, 1.0, num_queries), 5000)
    ours_epoch_10 = normalize_to_frequency(np.ones(num_queries) + rng.normal(0, 0.08, num_queries), 5000)
    ours_epoch_25 = normalize_to_frequency(np.ones(num_queries) + rng.normal(0, 0.05, num_queries), 5000)

    data = [
        [baseline_epoch_0, baseline_epoch_10, baseline_epoch_25],
        [ours_epoch_0, ours_epoch_10, ours_epoch_25],
    ]

    row_names = ["Baseline", "Ours"]
    col_names = ["Epoch 0", "Epoch 10", "Epoch 25"]

    sub_gs = outer_gs.subgridspec(2, 3, wspace=0.35, hspace=0.45)

    for r in range(2):
        for c in range(3):
            ax = fig.add_subplot(sub_gs[r, c])
            ax.bar(x, data[r][c], width=0.75)
            ax.set_title(col_names[c], fontsize=9)
            ax.set_xlim(0, num_queries + 1)
            ax.set_ylim(0, 5000)
            ax.set_xlabel("Query", fontsize=8)

            if c == 0:
                ax.set_ylabel(f"{row_names[r]}\nFrequency", fontsize=8)
            else:
                ax.set_ylabel("Frequency", fontsize=8)

            ax.tick_params(axis="both", labelsize=7)

    return sub_gs


def make_joint_surface(k_values, param_values, peak_k, peak_param, base=52.0, gain=8.0):
    """
    Creates smooth demo sensitivity values.

    This is only for code verification. Replace output with real measured R@10.
    """
    kk, pp = np.meshgrid(k_values, param_values, indexing="ij")
    surface = (
        base
        + gain
        * np.exp(-((kk - peak_k) ** 2) / 18.0)
        * np.exp(-((pp - peak_param) ** 2) / (2 * (0.18 ** 2)))
    )
    return surface


def plot_3d_bar(ax, k_values, param_values, scores, title, param_label):
    xpos, ypos = np.meshgrid(np.arange(len(k_values)), np.arange(len(param_values)), indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = np.zeros_like(xpos, dtype=float)

    dx = np.full_like(xpos, 0.55, dtype=float)
    dy = np.full_like(ypos, 0.55, dtype=float)
    dz = scores.ravel()

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, shade=True)

    ax.set_title(title, fontsize=9)
    ax.set_xlabel("K", fontsize=8)
    ax.set_ylabel(param_label, fontsize=8)
    ax.set_zlabel("R@10", fontsize=8)

    ax.set_xticks(np.arange(len(k_values)) + 0.25)
    ax.set_xticklabels([str(v) for v in k_values], fontsize=7)

    ax.set_yticks(np.arange(len(param_values)) + 0.25)
    ax.set_yticklabels([str(v) for v in param_values], fontsize=7)

    ax.tick_params(axis="z", labelsize=7)
    ax.view_init(elev=25, azim=-55)