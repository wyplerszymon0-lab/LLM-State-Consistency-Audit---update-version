"""Canonical transaction data for the state-consistency benchmark scenario.

This is the single source of truth for the scenario. Model submissions in
models/ hold their own hardcoded copies (they represent frozen LLM output,
same as a script an LLM handed back in response to a prompt), but anything
we author ourselves (the reference solver, the CSV exporter) should import
from here instead of duplicating the data.

Columns: txn_id, portfolio_id, type, quantity, unit_price
"""

BUY = 1
SELL = 2

TRANSACTIONS = [
    (1, 101, BUY, 10, 100),
    (2, 102, BUY, 20, 200),
    (3, 101, BUY, 10, 110),
    (4, 101, SELL, 15, 120),
    (5, 102, SELL, 10, 210),
    (6, 101, BUY, 20, 115),
    (7, 103, BUY, 50, 50),
    (8, 101, SELL, 10, 130),
    (9, 102, BUY, 15, 205),
    (10, 103, SELL, 20, 55),
    (11, 101, BUY, 10, 120),
    (12, 101, SELL, 15, 140),
    (13, 102, SELL, 20, 215),
    (14, 103, BUY, 10, 60),
    (15, 101, SELL, 5, 145),
]
