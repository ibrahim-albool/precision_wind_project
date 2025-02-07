import matplotlib
import matplotlib.pyplot as plt
from cleaned_returns import losses
matplotlib.use('TkAgg')
def main():
    print("test")

    epochs = range(1, len(losses) + 1)
    plt.rcParams['font.family'] = 'serif'
    # Create the plot
    plt.figure(figsize=(6, 4))  # IEEE-friendly size
    # plt.plot(epochs, losses, marker='o', linestyle='-', linewidth=2, markersize=5, label="Training Loss")
    plt.plot(epochs, losses, linestyle='-', linewidth=3, markersize=5, label="Training Return")
    plt.tick_params(labelsize=15)
    # Labels and title
    plt.xlabel("Iterations", fontsize=15)
    plt.ylabel("Return", fontsize=15)
    # plt.title("Return Curve", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.8)  # Light grid
    plt.legend(fontsize=15 - 1, loc="lower right")
    plt.tight_layout()

    # Save as PDF
    plt.savefig("return_curve.pdf", format="pdf", dpi=300, bbox_inches="tight")

    plt.show()







if __name__ == "__main__":

    main()