"""Scores model submissions against the reference solver and renders a report."""

from dataclasses import dataclass
from datetime import date

from audit import reference
from audit.discover import discover_models


@dataclass
class ScoreResult:
    name: str
    result: float
    reference_result: float
    absolute_error: float
    quality_score: float


def score_all() -> list[ScoreResult]:
    ref_value = reference.run()
    scores = []
    for name, module in discover_models():
        value = module.run()
        error = abs(value - ref_value)
        quality = max(0.0, 1 - error / ref_value) if ref_value else 0.0
        scores.append(
            ScoreResult(
                name=name,
                result=value,
                reference_result=ref_value,
                absolute_error=round(error, 2),
                quality_score=round(quality, 4),
            )
        )
    scores.sort(key=lambda s: -s.quality_score)
    return scores


def render_report(scores: list[ScoreResult], path: str = "reports/analysis.md") -> str:
    lines = [
        "# LLM State-Consistency Audit — Results",
        "",
        f"_Generated {date.today().isoformat()} by `run_audit.py`. Do not hand-edit — rerun the audit instead._",
        "",
        "## Scenario",
        "",
        "15 buy/sell transactions across 3 portfolios, testing a model's ability to "
        "track global state across three interacting rules:",
        "",
        "1. **Price Modifier** — a BUY immediately after a *profitable* SELL costs 1% more.",
        "2. **Global Wealth Tax** — a 2% penalty on a sale's profit whenever total wealth "
        "(cash + current holdings' market value) exceeds 10,000.",
        "3. **Holding Cost Drift** — every open lot's cost basis compounds by 0.1% after "
        "every transaction.",
        "",
        "Getting any one of these state dependencies stale or mistimed produces a "
        "silently wrong final number without raising an exception — that's what this "
        "harness measures.",
        "",
        "## Leaderboard",
        "",
        "| Rank | Model | Result | Reference | Absolute Error | Quality Score |",
        "| :--- | :--- | ---: | ---: | ---: | ---: |",
    ]
    for i, s in enumerate(scores, start=1):
        lines.append(
            f"| {i} | {s.name} | {s.result:.2f} | {s.reference_result:.2f} | "
            f"{s.absolute_error:.2f} | {s.quality_score:.4f} |"
        )
    lines.append("")
    lines.append("## Scoring")
    lines.append("")
    lines.append("```")
    lines.append("absolute_error = |model_result - reference_result|")
    lines.append("quality_score  = max(0, 1 - absolute_error / reference_result)")
    lines.append("```")
    lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path
