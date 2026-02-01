"""
Kelly Criterion Visualization
Plots: (1) Optimal fraction vs probability for different odds
       (2) Wealth evolution over time for different bet fractions

Run: python kelly_criterion_plots.py
Use --no-show to only save the PNG and exit (e.g. in terminals without display).
"""

import argparse
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def kelly_fraction(p: float, b: float) -> float:
    """
    Kelly criterion: optimal fraction of bankroll to bet.
    p = probability of win, b = decimal odds - 1 (net profit per unit when you win).
    f* = (p*b - q) / b = p - (1-p)/b
    """
    q = 1 - p
    if b <= 0:
        return 0.0
    f = (p * b - q) / b
    return max(0.0, min(1.0, f))  # clamp to [0, 1]


def simulate_wealth(
    p: float, b: float, f: float, n_trials: int, initial_wealth: float = 1.0, seed: int | None = 42
) -> np.ndarray:
    """
    Simulate wealth over n_trials with fixed fraction f (win with prob p, odds b).
    If seed is None, uses OS entropy for a fresh random sequence every time.
    """
    wealth = np.zeros(n_trials + 1)
    wealth[0] = initial_wealth
    # None => nondeterministic seed from OS (different every run)
    rng = np.random.default_rng(seed)
    for t in range(n_trials):
        bet_size = wealth[t] * f
        win = rng.random() < p
        if win:
            wealth[t + 1] = wealth[t] + bet_size * b
        else:
            wealth[t + 1] = wealth[t] - bet_size
    return wealth


def run_kelly_experiments(
    p: float = 0.55,
    b: float = 1.0,
    n_trials: int = 50000,
    n_curves: int = 10,
    n_images: int = 10,
    output_dir: str = "kelly_experiments",
    show_plot: bool = True,
) -> list[str]:
    """
    Draw n_images separate figures. Each figure shows multiple Kelly multiplier curves
    (0.1×–1.0×, 0.9×, 1.5×, 1.9×, 2×, 2.1×, 4× Kelly, and All in). Each simulation uses
    OS entropy (no fixed seed), so you get a fresh random outcome every time.
    """
    os.makedirs(output_dir, exist_ok=True)
    f_star = kelly_fraction(p, b)
    ev_per_unit = p * b - (1 - p)
    # Always print so user sees actual p, b (CLI overrides function defaults)
    print(f"Run params: p={p}, b={b} => f*={f_star:.4f}, EV={ev_per_unit:.4f}")
    if b <= 0 or ev_per_unit <= 0:
        print("Warning: no positive edge (b<=0 or EV<=0). Wealth cannot grow.")
    # Base: 5 points from 0.1× to 1.0×; then 1.5×, 1.9×, 2×, 2.1×, 4× Kelly, and All in
    base_multiples = np.linspace(0.1, 1.0, 5)
    curve_specs = [(f"{m:.1f}× Kelly", m * f_star) for m in base_multiples]
    for m in [1.5, 1.9, 2.0, 2.1, 4.0]:
        curve_specs.append((f"{m}× Kelly" if m == int(m) else f"{m}× Kelly", m * f_star))
    curve_specs.append(("All in", 1.0))
    out_paths = []

    for img in range(n_images):
        fig, ax = plt.subplots(figsize=(10, 6))
        for label, f in curve_specs:
            f_clamped = min(f, 1.0)
            wealth = simulate_wealth(p, b, f_clamped, n_trials, seed=None)
            ax.plot(wealth, label=label, lw=1.5, alpha=0.9)
        ax.set_xlabel("Time (number of bets)")
        ax.set_ylabel("Wealth (multiple of initial)")
        ax.set_title(f"Kelly experiments (image {img + 1}): p = {p}, b = {b}, f* = {f_star:.3f}")
        ax.legend(loc="upper left", ncol=3, fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_yscale("log")
        ax.set_ylim(0.01, None)

        out_path = os.path.join(output_dir, f"kelly_experiments_{img + 1:02d}.png")
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        out_paths.append(out_path)
        print(f"Saved {out_path}")
        plt.close(fig)

    if show_plot and out_paths:
        fig, ax = plt.subplots(figsize=(10, 6))
        for label, f in curve_specs:
            f_clamped = min(f, 1.0)
            wealth = simulate_wealth(p, b, f_clamped, n_trials, seed=None)
            ax.plot(wealth, label=label, lw=1.5, alpha=0.9)
        ax.set_xlabel("Time (number of bets)")
        ax.set_ylabel("Wealth (multiple of initial)")
        ax.set_title(f"Kelly experiments (image 1): p = {p}, b = {b}, f* = {f_star:.3f}")
        ax.legend(loc="upper left", ncol=3, fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_yscale("log")
        ax.set_ylim(0.01, None)
        plt.show()
        plt.close(fig)
    return out_paths


def main(show_plot: bool = True):
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.25)

    # --- Plot 1: Kelly fraction vs probability for different odds (b) ---
    ax1 = fig.add_subplot(gs[0, 0])
    p_grid = np.linspace(0.01, 0.99, 200)
    odds_list = [0.5, 1.0, 2.0, 3.0, 5.0]  # b = net profit per unit when you win
    for b in odds_list:
        f_star = np.array([kelly_fraction(p, b) for p in p_grid])
        ax1.plot(p_grid, f_star, label=f"b = {b}", lw=2)
    ax1.set_xlabel("Probability of win (p)")
    ax1.set_ylabel("Optimal fraction (f*)")
    ax1.set_title("Kelly fraction vs probability for different odds")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)

    # --- Plot 2: Kelly fraction vs odds (b) for different p ---
    ax2 = fig.add_subplot(gs[0, 1])
    b_grid = np.linspace(0.1, 10, 300)
    probs = [0.4, 0.5, 0.55, 0.6, 0.7]
    for p in probs:
        f_star = np.array([kelly_fraction(p, b) for b in b_grid])
        ax2.plot(b_grid, f_star, label=f"p = {p}", lw=2)
    ax2.set_xlabel("Odds (b)")
    ax2.set_ylabel("Optimal fraction (f*)")
    ax2.set_title("Kelly fraction vs odds for different win probabilities")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1)

    # --- Plot 3: Wealth over time, different fractions (single scenario) ---
    ax3 = fig.add_subplot(gs[1, :])
    p, b = 0.55, 1.0  # 55% win, even-money bet
    n_times = 500
    f_kelly = kelly_fraction(p, b)
    fractions = [0, 0.25 * f_kelly, 0.5 * f_kelly, f_kelly, 1.5 * f_kelly]
    labels = ["No bet", "¼ Kelly", "½ Kelly", "Full Kelly", "1.5× Kelly"]
    for f, label in zip(fractions, labels):
        wealth = simulate_wealth(p, b, f, n_times)
        ax3.plot(wealth, label=label, lw=1.5, alpha=0.9)
    ax3.set_xlabel("Time (number of bets)")
    ax3.set_ylabel("Wealth (multiple of initial)")
    ax3.set_title(f"Wealth evolution over time (p = {p}, b = {b}, f* = {f_kelly:.3f})")
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_yscale("log")
    ax3.set_ylim(0.01, None)

    plt.suptitle("Kelly Criterion: optimal bet sizing and growth", fontsize=14, y=1.02)
    plt.savefig("kelly_criterion_plots.png", dpi=150, bbox_inches="tight")
    print("Saved kelly_criterion_plots.png")
    if show_plot:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot Kelly criterion")
    parser.add_argument("--no-show", action="store_true", help="Only save PNG, do not open window")
    parser.add_argument(
        "--experiments",
        action="store_true",
        help="Run 10 Kelly experiments (curves for different fractions), save to kelly_experiments/",
    )
    parser.add_argument("-p", "--prob", type=float, default=0.55, help="Win probability (default: 0.55)")
    parser.add_argument("-b", "--odds", type=float, default=1.0, help="Odds b (default: 1.0)")
    parser.add_argument(
        "-o", "--output-dir", type=str, default="kelly_experiments", help="Output folder (default: kelly_experiments)"
    )
    args = parser.parse_args()
    if args.no_show:
        matplotlib.use("Agg")
    if args.experiments:
        run_kelly_experiments(
            p=args.prob,
            b=args.odds,
            output_dir=args.output_dir,
            show_plot=not args.no_show,
        )
    else:
        main(show_plot=not args.no_show)
