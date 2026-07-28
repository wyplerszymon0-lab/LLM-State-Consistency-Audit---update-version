"""CLI entry point: score every model in models/ against the reference solver.

Usage:
    python run_audit.py
"""

from audit.scorer import render_report, score_all


def main():
    scores = score_all()
    name_width = max((len(s.name) for s in scores), default=10)
    for s in scores:
        print(
            f"{s.name:<{name_width}}  result={s.result:>10.2f}  "
            f"error={s.absolute_error:>8.2f}  score={s.quality_score:.4f}"
        )
    path = render_report(scores)
    print(f"\nReport written to {path}")


if __name__ == "__main__":
    main()
