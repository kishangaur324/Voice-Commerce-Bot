# inventory/loader.py
import pandas as pd
import re

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def load_products(path):
    df = pd.read_csv(path)

    print("RAW COLUMNS:")
    for col in df.columns:
        print(repr(col))

    print(df.head())

    df = df.rename(columns={
        "Product Title": "title",
        "Category": "category",
        "Price": "price",
        "Stock Availibility": "stock",
        "Product Asin": "asin",
        "Brand": "brand"
    })

    print(df.head())

    df = df[["title", "category", "price", "stock", "asin", "brand"]]

    print("RAW COLUMNS:")
    for col in df.columns:
        print(repr(col))

    df["in_stock"] = df["stock"].str.lower().str.contains("in stock")

    # 🔥 normalize searchable fields
    df["title_norm"] = df["title"].apply(normalize)
    df["category_norm"] = df["category"].apply(normalize)

    return df
