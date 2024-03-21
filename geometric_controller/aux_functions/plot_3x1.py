import matplotlib.pyplot as plt

def plot_3x1(x, y, title_, xlabel_, ylabel_, linetype, linewidth, font_size=10):
    for i in range(3):
        plt.subplot(3, 1, i + 1)
        plt.plot(x, y[i, :], linetype, linewidth=linewidth)
        # plt.gca().set_fontname('Times New Roman')
        # plt.gca().set_fontsize(font_size)
        # plt.ylabel(r'${}_{}$'.format(ylabel_, i + 1), interpreter='latex')
        # plt.hold(True)

    # plt.xlabel(xlabel_, interpreter='latex')
    # plt.title(title_, interpreter='latex')
    plt.subplot(3, 1, 2)
    # plt.ylabel(r'${}$'.format(ylabel_), interpreter='latex')
    plt.show()
