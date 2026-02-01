# Investment experiment — Kelly criterion

Kelly criterion plots and experiments: optimal bet fraction (f*), wealth over time for different Kelly multipliers.

## Quick start

```bash
pip install -r requirements.txt
python kelly_criterion_plots.py --no-show
python kelly_criterion_plots.py --experiments --no-show
```

See **[COMMANDS.md](COMMANDS.md)** for all options and examples.

## Repo layout

| Path | Description |
|------|-------------|
| `kelly_criterion_plots.py` | Main script: Kelly formula, simulation, plots. |
| `COMMANDS.md` | CLI options and usage. |
| `requirements.txt` | numpy, matplotlib. |
| `kelly_criterion_plots.png` | Single figure from default run (f* vs p/b, wealth). |
| `kelly_experiments/` | 10 experiment images (multiple curves per image). |

Images (`.png`) are tracked; regenerate with the commands above.
