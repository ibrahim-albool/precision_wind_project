import matplotlib.pyplot as plt

def plot_3x3(x, y, title_, xlabel_, ylabel_, linetype, linewidth, font_size=10, desired=False):
    fig, axs = plt.subplots(3, 3, figsize=(12, 12))

    for i in range(3):
        for j in range(3):
            k = 3 * i + j + 1
            axs[i, j].plot(x, y[i, j, :], linetype, linewidth=linewidth, color='red' if desired else 'blue')
            # axs[i, j].set_title(r'${}_{}{}$'.format(ylabel_, i + 1, j + 1), interpreter='latex')
            # axs[i, j].set_xlabel(xlabel_, interpreter='latex')
            # axs[i, j].set_ylabel(r'${}_{}$'.format(ylabel_, j + 1), interpreter='latex')
            # axs[i, j].grid(True)
            axs[i, j].set_ylim([-1, 1])
            # axs[i, j].set_fontname('Times New Roman')
            # axs[i, j].set_fontsize(font_size)
            # axs[i, j].hold(True)

    # plt.suptitle(title_, interpreter='latex', fontsize=font_size)
    # plt.xlabel(xlabel_, interpreter='latex')
    # plt.ylabel(r'${}$'.format(ylabel_), interpreter='latex')
    plt.show()

