# LLM State-Consistency Audit — Results

_Generated 2026-07-28 by `run_audit.py`. Do not hand-edit — rerun the audit instead._

## Scenario

15 buy/sell transactions across 3 portfolios, testing a model's ability to track global state across three interacting rules:

1. **Price Modifier** — a BUY immediately after a *profitable* SELL costs 1% more.
2. **Global Wealth Tax** — a 2% penalty on a sale's profit whenever total wealth (cash + current holdings' market value) exceeds 10,000.
3. **Holding Cost Drift** — every open lot's cost basis compounds by 0.1% after every transaction.

Getting any one of these state dependencies stale or mistimed produces a silently wrong final number without raising an exception — that's what this harness measures.

## Leaderboard

| Rank | Model | Result | Reference | Absolute Error | Quality Score |
| :--- | :--- | ---: | ---: | ---: | ---: |
| 1 | Gemini 3.1 Pro Reasoning | 17072.00 | 17072.00 | 0.00 | 1.0000 |
| 2 | Baseline (Partial State Update) | 17035.94 | 17072.00 | 36.06 | 0.9979 |

## Scoring

```
absolute_error = |model_result - reference_result|
quality_score  = max(0, 1 - absolute_error / reference_result)
```
