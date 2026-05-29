def plot_joint_sensitivity_block(fig, outer_gs):


    k_values = np.array([2, 4, 6, 8, 10])
    alpha_values = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    eta_values = np.array([0.03, 0.05, 0.07, 0.09, 0.11])
    lambda_values = np.array([0.1, 0.3, 0.5, 0.7, 0.9])

    scores_alpha = make_joint_surface(k_values, alpha_values, peak_k=6, peak_param=0.3)
    scores_eta = make_joint_surface(k_values, eta_values, peak_k=6, peak_param=0.07)
    scores_lambda = make_joint_surface(k_values, lambda_values, peak_k=6, peak_param=0.5)

    sub_gs = outer_gs.subgridspec(1, 3, wspace=0.15)

    ax1 = fig.add_subplot(sub_gs[0, 0], projection="3d")
    ax2 = fig.add_subplot(sub_gs[0, 1], projection="3d")
    ax3 = fig.add_subplot(sub_gs[0, 2], projection="3d")

    plot_3d_bar(ax1, k_values, alpha_values, scores_alpha, "K with alpha", "alpha")
    plot_3d_bar(ax2, k_values, eta_values, scores_eta, "K with eta", "eta")
    plot_3d_bar(ax3, k_values, lambda_values, scores_lambda, "K with lambda", "lambda")

    return sub_gs


def main():
    fig = plt.figure(figsize=(14, 5.5))
    gs = GridSpec(
        1,
        2,
        figure=fig,
        width_ratios=[1.05, 1.25],
        wspace=0.18,
        left=0.04,
        right=0.98,
        top=0.90,
        bottom=0.16,
    )

    plot_query_distribution_block(fig, gs[0, 0])
    plot_joint_sensitivity_block(fig, gs[0, 1])

    fig.suptitle("Additional Analysis of SNS-CIR on CIRR", fontsize=13)

    fig.text(
        0.25,
        0.06,
        "(a) Query distribution on CIRR during training.",
        ha="center",
        fontsize=10,
    )
    fig.text(
        0.73,
        0.06,
        "(b) Joint sensitivity analysis of SNS-CIR.",
        ha="center",
        fontsize=10,
    )

    plt.savefig("sns_cir_two_blocks.pdf", bbox_inches="tight")
    plt.savefig("sns_cir_two_blocks.png", dpi=300, bbox_inches="tight")
    plt.show()