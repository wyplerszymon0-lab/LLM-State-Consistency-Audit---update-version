import pandas as pd

data = {
    'txn_id': range(1, 16),
    'portfolio_id': [101, 102, 101, 101, 102, 101, 103, 101, 102, 103, 101, 101, 102, 103, 101],
    'type': [1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2], # 1 = BUY, 2 = SELL
    'quantity': [10, 20, 10, 15, 10, 20, 50, 10, 15, 20, 10, 15, 20, 10, 5],
    'unit_price': [100, 200, 110, 120, 210, 115, 50, 130, 205, 55, 120, 140, 215, 60, 145]
}

df = pd.DataFrame(data)
df.to_csv('transactions.csv', index=False)
print("Plik transactions.csv został wygenerowany.")
