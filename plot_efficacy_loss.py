"""Plot the efficacy loss utility for five curvature parameters."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


EFFICACY_THRESHOLD = 0.4
ALPHA_LE_VALUES = (0.5, 0.75, 1.0, 1.25, 1.5)


def efficacy_loss_utility(pi_e, alpha_le):
    """Evaluate the loss formula, including its zero limit at the threshold."""
    if not 0 <= pi_e <= EFFICACY_THRESHOLD:
        raise ValueError("pi_e must be between 0 and 0.4.")
    if alpha_le <= 0:
        raise ValueError("alpha_le must be positive.")
    return -((EFFICACY_THRESHOLD - pi_e) / EFFICACY_THRESHOLD) ** alpha_le


def plot_efficacy_loss(output_path):
    """Save the five loss-region curves as a 300 dpi PNG."""
    pi_e_values = [EFFICACY_THRESHOLD * i / 1000 for i in range(1001)]
    line_styles = ("-", "--", "-.", ":", (0, (5, 1, 1, 1)))
    fig, ax = plt.subplots(figsize=(9, 6), layout="constrained")

    for alpha_le, line_style in zip(ALPHA_LE_VALUES, line_styles):
        utilities = [
            efficacy_loss_utility(pi_e, alpha_le) for pi_e in pi_e_values
        ]
        ax.plot(
            pi_e_values,
            utilities,
            linewidth=2,
            linestyle=line_style,
            label=rf"$\alpha_{{LE}} = {alpha_le:g}$",
        )

    ax.set(
        xlabel=r"Efficacy probability $\pi_E$",
        ylabel=r"Efficacy utility $u_E(\pi_E)$",
        title=r"Efficacy utility in the loss region ($\bar{\pi}_E = 0.4$)",
        xlim=(0, EFFICACY_THRESHOLD),
        ylim=(-1.05, 0.05),
    )
    ax.set_xticks([i / 20 for i in range(9)])
    ax.grid(True, alpha=0.3)
    ax.legend(title="Loss curvature parameter")
    fig.savefig(output_path, dpi=300, format="png")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("efficacy_loss_utility.png"),
        help="Output PNG path (default: beside this script).",
    )
    args = parser.parse_args()
    plot_efficacy_loss(args.output)
    print(f"Saved plot to {args.output.resolve()}")


if __name__ == "__main__":
    main()
