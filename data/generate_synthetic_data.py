"""generate_synthetic_data.py

Generates synthetic retail data for the Capstone Global Health Retail project.

Usage:
    python data/generate_synthetic_data.py --n_customers 500 --n_products 200 --n_stores 20 --n_transactions 5000 --out_dir data/output

Outputs CSVs into the out_dir.
"""

import argparse
import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker


def random_dates(start, end, n, seed=None):
    rng = np.random.default_rng(seed)
    start_u = int(start.timestamp())
    end_u = int(end.timestamp())
    ints = rng.integers(start_u, end_u + 1, size=n)
    return [datetime.fromtimestamp(int(ts)) for ts in ints]


def generate_products(n_products, fake, seed=None):
    random.seed(seed)
    np.random.seed(None if seed is None else seed + 1)

    categories = [
        "Medicines",
        "Vitamins & Supplements",
        "Hygiene",
        "Maternal & Baby",
        "Diagnostics",
        "Personal Care",
        "Medical Supplies",
        "Nutrition",
    ]

    brands = [fake.company() for _ in range(max(20, n_products // 5))]

    products = []
    for i in range(1, n_products + 1):
        category = random.choice(categories)
        brand = random.choice(brands)
        name = f"{category.split()[0]} Product {i}"
        unit_price = round(float(np.random.lognormal(mean=2.0, sigma=0.8)), 2)  # varied prices
        products.append({
            "product_id": f"P{i:05d}",
            "product_name": name,
            "category": category,
            "brand": brand,
            "unit_price": unit_price,
        })
    return pd.DataFrame(products)


def generate_stores(n_stores, fake, seed=None):
    random.seed(seed)
    stores = []
    countries = [
        "United States",
        "India",
        "Kenya",
        "Nigeria",
        "Brazil",
        "South Africa",
        "United Kingdom",
        "Philippines",
        "Mexico",
        "Indonesia",
    ]
    for i in range(1, n_stores + 1):
        country = random.choice(countries)
        store_name = f"{fake.city()} Store {i}"
        storesize = random.choice(["Small", "Medium", "Large"])
        stores.append({
            "store_id": f"S{i:04d}",
            "store_name": store_name,
            "country": country,
            "store_size": storesize,
        })
    return pd.DataFrame(stores)


def generate_customers(n_customers, fake, start_signup, end_signup, seed=None):
    random.seed(seed)
    customers = []
    genders = ["F", "M", "Other"]
    countries = [
        "United States",
        "India",
        "Kenya",
        "Nigeria",
        "Brazil",
        "South Africa",
        "United Kingdom",
        "Philippines",
        "Mexico",
        "Indonesia",
    ]
    for i in range(1, n_customers + 1):
        first = fake.first_name()
        last = fake.last_name()
        gender = random.choices(genders, weights=[0.49, 0.49, 0.02])[0]
        birth_year = random.randint(1940, 2015)
        birthdate = datetime(birth_year, random.randint(1, 12), random.randint(1, 28))
        age = (datetime.now() - birthdate).days // 365
        signup = fake.date_between(start_date=start_signup, end_date=end_signup)
        country = random.choice(countries)
        customers.append({
            "customer_id": f"C{i:06d}",
            "first_name": first,
            "last_name": last,
            "gender": gender,
            "birthdate": birthdate.date().isoformat(),
            "age": age,
            "country": country,
            "signup_date": signup.isoformat(),
        })
    return pd.DataFrame(customers)


def generate_transactions(n_transactions, customers_df, products_df, stores_df, start_date, end_date, seed=None):
    random.seed(seed)
    np.random.seed(None if seed is None else seed + 2)
    tx_dates = random_dates(start_date, end_date, n_transactions, seed=seed)

    payment_methods = ["cash", "card", "mobile", "insurance"]

    rows = []
    for i in range(1, n_transactions + 1):
        customer = customers_df.sample(1).iloc[0]
        product = products_df.sample(1).iloc[0]
        store = stores_df.sample(1).iloc[0]
        quantity = int(np.random.choice([1, 1, 2, 3, 4, 5, 10], p=[0.4,0.2,0.15,0.1,0.08,0.05,0.02]))
        unit_price = float(product["unit_price"])
        # add noise to price to simulate discounts or markup
        price_noise = round(unit_price * np.random.normal(1.0, 0.05), 2)
        promotion = random.random() < 0.15
        if promotion:
            price_noise = round(price_noise * random.choice([0.7, 0.75, 0.8, 0.85]), 2)
        total = round(price_noise * quantity, 2)
        rows.append({
            "transaction_id": f"T{i:08d}",
            "transaction_date": tx_dates[i - 1].isoformat(sep=' '),
            "customer_id": customer["customer_id"],
            "store_id": store["store_id"],
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": price_noise,
            "total_amount": total,
            "promotion": promotion,
            "payment_method": random.choice(payment_methods),
        })

    return pd.DataFrame(rows)


def enrich_transactions(trans_df, customers_df, products_df, stores_df):
    df = trans_df.merge(customers_df, on="customer_id", how="left")
    df = df.merge(products_df, on="product_id", how="left")
    df = df.merge(stores_df, on="store_id", how="left")
    return df


def main(args):
    fake = Faker()
    Faker.seed(args.seed)
    random.seed(args.seed)
    np.random.seed(args.seed)

    os.makedirs(args.out_dir, exist_ok=True)

    start_signup = datetime.strptime(args.start_signup, "%Y-%m-%d").date()
    end_signup = datetime.strptime(args.end_signup, "%Y-%m-%d").date()
    start_tx = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_tx = datetime.strptime(args.end_date, "%Y-%m-%d")

    print("Generating products...")
    products_df = generate_products(args.n_products, fake, seed=args.seed)
    products_df.to_csv(os.path.join(args.out_dir, "products.csv"), index=False)

    print("Generating stores...")
    stores_df = generate_stores(args.n_stores, fake, seed=args.seed)
    stores_df.to_csv(os.path.join(args.out_dir, "stores.csv"), index=False)

    print("Generating customers...")
    customers_df = generate_customers(args.n_customers, fake, start_signup, end_signup, seed=args.seed)
    customers_df.to_csv(os.path.join(args.out_dir, "customers.csv"), index=False)

    print("Generating transactions...")
    transactions_df = generate_transactions(
        args.n_transactions, customers_df, products_df, stores_df, start_tx, end_tx, seed=args.seed
    )
    transactions_df.to_csv(os.path.join(args.out_dir, "transactions.csv"), index=False)

    print("Enriching transactions (joining product/customer/store attributes)...")
    enriched = enrich_transactions(transactions_df, customers_df, products_df, stores_df)
    enriched.to_csv(os.path.join(args.out_dir, "transactions_enriched.csv"), index=False)

    print("Done. Files written to:")
    for f in ["products.csv", "stores.csv", "customers.csv", "transactions.csv", "transactions_enriched.csv"]:
        print(f"  - {os.path.join(args.out_dir, f)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic retail data for capstone")
    parser.add_argument("--n_customers", type=int, default=500, help="Number of customers to generate")
    parser.add_argument("--n_products", type=int, default=200, help="Number of unique products to generate")
    parser.add_argument("--n_stores", type=int, default=20, help="Number of stores to generate")
    parser.add_argument("--n_transactions", type=int, default=5000, help="Number of transactions to generate")
    parser.add_argument("--start_signup", type=str, default="2018-01-01", help="Earliest customer signup date (YYYY-MM-DD)")
    parser.add_argument("--end_signup", type=str, default="2023-12-31", help="Latest customer signup date (YYYY-MM-DD)")
    parser.add_argument("--start_date", type=str, default="2023-01-01", help="Earliest transaction date (YYYY-MM-DD)")
    parser.add_argument("--end_date", type=str, default="2023-12-31", help="Latest transaction date (YYYY-MM-DD)")
    parser.add_argument("--out_dir", type=str, default="data/output", help="Directory to write CSVs to")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")

    args = parser.parse_args()
    main(args)
