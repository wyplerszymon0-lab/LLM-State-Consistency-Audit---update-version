import pandas as pd


def calculate_v3_benchmark():
    data = [
        (1, 101, 1, 10, 100), (2, 102, 1, 20, 200), (3, 101, 1, 10, 110),
        (4, 101, 2, 15, 120), (5, 102, 2, 10, 210), (6, 101, 1, 20, 115),
        (7, 103, 1, 50, 50), (8, 101, 2, 10, 130), (9, 102, 1, 15, 205),
        (10, 103, 2, 20, 55), (11, 101, 1, 10, 120), (12, 101, 2, 15, 140),
        (13, 102, 2, 20, 215), (14, 103, 1, 10, 60), (15, 101, 2, 5, 145)
    ]
    df = pd.DataFrame(data, columns=['txn_id', 'portfolio_id', 'type', 'qty', 'price'])

    portfolios = {}
    total_cash = 0
    last_sale_was_profitable = False

    for _, row in df.iterrows():
        p_id = row['portfolio_id']
        if p_id not in portfolios: portfolios[p_id] = []

        # 1. PRICE MODIFIER: If last sale was profit, new buy is 1% more expensive
        current_price = row['price']
        if row['type'] == 1 and last_sale_was_profitable:
            current_price *= 1.01

        if row['type'] == 1:
            portfolios[p_id].append([row['qty'], current_price])
        else:
            qty_to_sell = row['qty']
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

            revenue = row['qty'] * current_price
            gross_profit = revenue - total_cost_basis
            last_sale_was_profitable = gross_profit > 0

            # 2. GLOBAL THRESHOLD TAX: Calculate total market value BEFORE tax
            current_inv_val = sum(sum(b[0] * b[1] for b in units) for units in portfolios.values())
            global_tax_penalty = 0.02 if (total_cash + current_inv_val) > 10000 else 0

            tax_rate = (0.15 if gross_profit > 200 else 0.05) + global_tax_penalty
            tax_amount = max(0, gross_profit * tax_rate)
            total_cash += revenue - tax_amount

        # 3. DEGRADATION
        for pid in portfolios:
            for batch in portfolios[pid]:
                batch[1] = round(batch[1] * 1.001, 4)

    final_val = round(total_cash + sum(sum(b[0] * b[1] for b in units) for units in portfolios.values()), 2)
    return final_val


print(f"Result: {calculate_v3_benchmark()}")
