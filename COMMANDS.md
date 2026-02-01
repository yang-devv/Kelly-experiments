# Kelly Criterion — Commands

## Run

```bash
python kelly_criterion_plots.py
```

- **Default:** One figure (f* vs p, f* vs b, wealth over time). Saves `kelly_criterion_plots.png`, then opens window.

## Options

| Option | Description |
|--------|-------------|
| `--no-show` | Save PNG(s) only; do not open plot window. |
| `--experiments` | Run 10 Kelly experiment images (multiple curves per image). Saves to `kelly_experiments/` (or `-o` path). |
| `-p`, `--prob` | Win probability (default: 0.55). |
| `-b`, `--odds` | Odds b (default: 1.0). |
| `-o`, `--output-dir` | Output folder for experiments (default: `kelly_experiments`). |

- **CLI vs code:** When you run from the command line, `-p` and `-b` use the **parser defaults** (0.55, 1.0). To use other values (e.g. p=0, b=0.1), you must pass them explicitly: `-p 0 -b 0.1`.
- **Experiments:** With `--experiments`, the script prints `Run params: p=..., b=... => f*=..., EV=...` so you can confirm the values used.

## Examples

```bash
# Main plot, save only (no window)
python kelly_criterion_plots.py --no-show

# 10 experiment images, save only
python kelly_criterion_plots.py --experiments --no-show

# Experiments with custom p, b, and output folder
python kelly_criterion_plots.py --experiments -p 0.6 -b 2 -o my_runs --no-show

# No edge (p=0 or EV<=0): must pass -p -b; script prints f*, EV and a warning
python kelly_criterion_plots.py --experiments -p 0 -b 0.1 --no-show
```

## From code

```python
from kelly_criterion_plots import main, run_kelly_experiments

main(show_plot=False)                    # main figure
run_kelly_experiments(p=0.55, b=1.0, output_dir="kelly_experiments", show_plot=False)
```
