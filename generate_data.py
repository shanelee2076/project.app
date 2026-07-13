"""
generate_data.py
Generates a realistic synthetic sales dataset for the Sales Data Analytics Dashboard.
Run this once to (re)create data/sales_data.csv
"""

import numpy as np
import pandas as pd

np.random.seed(42)

# ---- Reference data ----
regions = ["North", "South", "East", "West", "Central"]

categories = {
    "Electronics": ["Laptop", "Smartphone", "Headphones", "Smartwatch", "Tablet"],
    "Furniture": ["Office Chair", "Desk", "Bookshelf", "Sofa", "Dining Table"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Cap"],
    "Groceries": ["Coffee", "Snack Pack", "Cereal", "Juice", "Spices"],
    "Stationery": ["Notebook", "Pen Set", "Backpack", "Marker Pack", "Desk Organizer"],
}

customer_segments = ["Consumer", "Corporate", "Small Business"]
ship_modes = ["Standard", "Express", "Same Day"]

# ---- Date range: 2 full years ----
date_range = pd.date_range(start="2024-01-01", end="2025-12-31", freq="D")

rows = []
order_id = 1000

for date in date_range:
    # seasonal + weekday effect on number of orders that day
    weekday_factor = 1.3 if date.weekday() < 5 else 0.8
    month_factor = 1.4 if date.month in [11, 12] else (1.15 if date.month in [6, 7] else 1.0)
    n_orders = max(1, int(np.random.poisson(6 * weekday_factor * month_factor)))

    for _ in range(n_orders):
        category = np.random.choice(list(categories.keys()))
        product = np.random.choice(categories[category])
        region = np.random.choice(regions, p=[0.24, 0.22, 0.20, 0.20, 0.14])
        segment = np.random.choice(customer_segments, p=[0.55, 0.30, 0.15])
        ship_mode = np.random.choice(ship_modes, p=[0.6, 0.3, 0.1])

        base_price = {
            "Electronics": np.random.uniform(80, 900),
            "Furniture": np.random.uniform(60, 500),
            "Clothing": np.random.uniform(10, 90),
            "Groceries": np.random.uniform(3, 40),
            "Stationery": np.random.uniform(2, 60),
        }[category]

        quantity = np.random.randint(1, 8)
        discount = np.random.choice([0, 0.05, 0.10, 0.15, 0.20], p=[0.4, 0.25, 0.2, 0.1, 0.05])

        sales = round(base_price * quantity * (1 - discount), 2)
        margin_rate = {
            "Electronics": np.random.uniform(0.08, 0.22),
            "Furniture": np.random.uniform(0.05, 0.18),
            "Clothing": np.random.uniform(0.15, 0.35),
            "Groceries": np.random.uniform(0.10, 0.25),
            "Stationery": np.random.uniform(0.20, 0.40),
        }[category]
        profit = round(sales * margin_rate - (sales * discount * 0.3), 2)

        rows.append({
            "Order_ID": f"ORD-{order_id}",
            "Order_Date": date.strftime("%Y-%m-%d"),
            "Region": region,
            "Category": category,
            "Product": product,
            "Customer_Segment": segment,
            "Ship_Mode": ship_mode,
            "Quantity": quantity,
            "Discount": discount,
            "Sales": sales,
            "Profit": profit,
        })
        order_id += 1

df = pd.DataFrame(rows)
df.to_csv("data/sales_data.csv", index=False)
print(f"Generated {len(df)} rows -> data/sales_data.csv")
print(df.head())
