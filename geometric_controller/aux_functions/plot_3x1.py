import matplotlib.pyplot as plt

# def plot_3x1(x, y, title_, xlabel_, ylabel_, linetype, linewidth, font_size=10):
#     for i in range(3):
#         plt.subplot(3, 1, i + 1)
#         plt.plot(x, y[i, :], linetype, linewidth=linewidth)
#         # plt.gca().set_fontname('Times New Roman')
#         # plt.gca().set_fontsize(font_size)
#         # plt.ylabel(r'${}_{}$'.format(ylabel_, i + 1))
#         # plt.hold(True)
#
#     plt.xlabel(xlabel_)
#     plt.title(title_)
#     plt.subplot(3, 1, 2)
#     plt.ylabel(ylabel_)
#     # plt.show()




def plot_3x1(x, y_signals, norms, switching, title_, xlabel_, ylabels, linetypes, linewidth, font_size=15, save_path="plot.pdf"):
    """
    Generates a 3x1 subplot figure, plotting multiple signals in each subplot with a legend.

    Args:
        x (array): X-axis data.
        y_signals (list of arrays): List of 3 matrices where each matrix has 3 rows (for x_r, x, error).
        title_ (str): Title of the plot.
        xlabels (list of str): X-axis label.
        ylabel_ (str): Y-axis base label.
        linetypes (list of str): List of line styles for each signal.
        linewidth (float): Line width.
        font_size (int, optional): Font size for text elements. Default is 10.
        save_path (str, optional): File path to save the figure as a PDF.
    """

    fig, axes = plt.subplots(4, 1, figsize=(6, 8), constrained_layout=True)

    plt.rcParams['font.family'] = 'serif'  # Use a serif font for IEEE formatting

    colors = ["green", "red", "purple"]  # Colors for x_r (reference), x, and error
    labels = [[r"$x^r$ (x-axis)", r"$x$ (x-axis)", r"$\overline{x}$ (x-axis)"],
              [r"$x^r$ (y-axis)", r"$x$ (y-axis)", r"$\overline{x}$ (y-axis)"],
              [r"$x^r$ (z-axis)", r"$x$ (z-axis)", r"$\overline{x}$ (z-axis)"],
              [r"$\|\|\mathbf{x}^r\|\|_2$", r"$\|\|\mathbf{x}\|\|_2$", r"$\|\|\mathbf{\overline{x}}\|\|_2$", "RL Swt."]]

    for i, ax in enumerate(axes[:-1]):
        for j in range(3):  # Loop over the three signals (x_r, x, error)
            ax.plot(x, y_signals[j][i], linetypes[j], color=colors[j], linewidth=linewidth, label=labels[i][j])

        ax.tick_params(labelsize=font_size)
        ax.grid(True, linestyle="--", alpha=0.8)  # IEEE-style grid
        # ax.set_ylabel(f"${ylabel_}_{i+1}$", fontsize=font_size)
        ax.set_ylabel(f"{ylabels[i]}", fontsize=font_size)
        ax.legend(fontsize=font_size - 1, loc="upper right")  # Add legend to each subplot
    for j in range(3):
        axes[3].plot(x, norms[j], linetypes[j], color=colors[j], linewidth=linewidth, label=labels[3][j])
    axes[3].plot(x, switching, color='gray', linewidth=linewidth, label=labels[3][3])
    axes[3].tick_params(labelsize=font_size)
    axes[3].grid(True, linestyle="--", alpha=0.8)  # IEEE-style grid
    # ax.set_ylabel(f"${ylabel_}_{i+1}$", fontsize=font_size)
    axes[3].set_ylabel(f"$\|\|.\|\|_2$ (m)", fontsize=font_size)
    axes[3].legend(fontsize=font_size - 1, loc="upper right")  # Add legend to each subplot

    axes[-1].set_xlabel(xlabel_, fontsize=font_size)
    # fig.suptitle(title_, fontsize=font_size + 2)

    # Save figure as high-quality PDF
    plt.savefig(save_path, format="pdf", dpi=300, bbox_inches="tight")
    plt.show()


