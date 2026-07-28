"""Reference ("ground truth") solver for the portfolio state-consistency scenario.

Rules enforced, in the order they interact:

1. Price Modifier — a BUY immediately following a *profitable* SELL costs 1%
   more (last_sale_was_profitable carries across transactions).
2. Global Wealth Tax — a 2% penalty on a sale's gross profit whenever total
   wealth (cash + current market value of holdings) exceeds 10,000. Wealth is
   evaluated *after* the sold lots are removed from the portfolio but
   *before* the sale's revenue is credited to cash.
3. Holding Cost Drift — every open lot's cost basis compounds by 0.1% after
   *every* transaction, buy or sell.
"""

from audit.scenario_data import BUY, TRANSACTIONS

MODEL_NAME = "Ground Truth (Reference)"

WEALTH_TAX_THRESHOLD = 10_000
WEALTH_TAX_RATE = 0.02
HIGH_PROFIT_THRESHOLD = 200
HIGH_PROFIT_TAX_RATE = 0.15
LOW_PROFIT_TAX_RATE = 0.05
PRICE_MODIFIER = 1.01
DRIFT_RATE = 1.001


def run() -> float:
    portfolios = {}
    cash = 0.0
    last_sale_was_profitable = False

    for _txn_id, p_id, t_type, qty, price in TRANSACTIONS:
        portfolios.setdefault(p_id, [])

        current_price = price
        if t_type == BUY and last_sale_was_profitable:
            current_price *= PRICE_MODIFIER

        if t_type == BUY:
            portfolios[p_id].append([qty, current_price])
        else:
            qty_to_sell = qty
            total_cost_basis = 0
            while qty_to_sell > 0 and portfolios[p_id]:
                batch = portfolios[p_id][0]
                if batch[0] <= qty_to_sell:
                    units = batch[0]
                    total_cost_basis += units * batch[1]
                    qty_to_sell -= units
                    portfolios[p_id].pop(0)
                else:
                    units = qty_to_sell
                    total_cost_basis += units * batch[1]
                    batch[0] -= units
                    qty_to_sell = 0

            revenue = qty * current_price
            gross_profit = revenue - total_cost_basis
            last_sale_was_profitable = gross_profit > 0

            current_inv_val = sum(
                b[0] * b[1] for units in portfolios.values() for b in units
            )
            wealth_penalty = (
                WEALTH_TAX_RATE if (cash + current_inv_val) > WEALTH_TAX_THRESHOLD else 0
            )

            base_rate = (
                HIGH_PROFIT_TAX_RATE if gross_profit > HIGH_PROFIT_THRESHOLD else LOW_PROFIT_TAX_RATE
            )
            tax_amount = max(0, gross_profit * (base_rate + wealth_penalty))
            cash += revenue - tax_amount

        for pid in portfolios:
            for batch in portfolios[pid]:
                batch[1] = round(batch[1] * DRIFT_RATE, 4)

    final_inv_val = sum(b[0] * b[1] for units in portfolios.values() for b in units)
    return round(cash + final_inv_val, 2)


if __name__ == "__main__":
    print(f"Result: {run()}")
