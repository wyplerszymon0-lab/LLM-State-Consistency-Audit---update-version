# LLM State-Consistency Audit

A small benchmark and harness for auditing whether an LLM-generated program
preserves **global state consistency** across a sequence of dependent
operations — the kind of bug that's invisible in isolated unit tests but
shows up under compounding, cross-record effects, and is easy to eyeball as
"looks right" when it silently isn't.

## Scenario

15 buy/sell transactions across 3 portfolios. A correct solution must track,
simultaneously:

1. **Price Modifier** — a BUY immediately after a *profitable* SELL costs 1% more.
2. **Global Wealth Tax** — a 2% penalty on a sale's profit whenever total
   wealth (cash + current market value of holdings) exceeds 10,000.
3. **Holding Cost Drift** — every open lot's cost basis compounds by 0.1%
   after *every* transaction.

Getting any one of these state dependencies stale or mistimed produces a
silently wrong final number, with no exception raised — that's what this
harness measures.

## Project layout

- `audit/scenario_data.py` — canonical transaction data (single source of truth).
- `audit/reference.py` — the reference ("ground truth") solver.
- `audit/discover.py` — auto-discovers model submissions in `models/`.
- `audit/scorer.py` — scores each submission against the reference and renders `reports/analysis.md`.
- `models/*.py` — one file per model submission. Each is self-contained (as
  an LLM would hand it back) and exposes `MODEL_NAME` and `run() -> float`.
- `data/generate_data.py` — exports the canonical scenario to `transactions.csv`.
- `run_audit.py` — CLI entry point.
- `reports/analysis.md` — generated leaderboard (overwritten on every run — don't hand-edit it).

## Usage

```bash
pip install -r requirements.txt   # only needed for data/generate_data.py
python run_audit.py
```

This runs the reference solver, runs every model in `models/`, and writes a
ranked leaderboard to `reports/analysis.md`.

## Adding a new model submission

Drop a new file in `models/`, e.g. `models/claude_x.py`:

```python
MODEL_NAME = "Claude X"

def run() -> float:
    ...
    return final_portfolio_value
```

Re-run `python run_audit.py` — it's picked up automatically, scored, and ranked.

## Scoring

```
absolute_error = |model_result - reference_result|
quality_score  = max(0, 1 - absolute_error / reference_result)
```
