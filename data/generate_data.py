"""Exports the canonical scenario transactions to transactions.csv.

Run from the repo root with: python -m data.generate_data
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from audit.scenario_data import TRANSACTIONS


def main():
    df = pd.DataFrame(
        TRANSACTIONS, columns=["txn_id", "portfolio_id", "type", "quantity", "unit_price"]
    )
    df.to_csv("transactions.csv", index=False)
    print("transactions.csv generated.")


if __name__ == "__main__":
    main()
