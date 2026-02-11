def find_product(query, df):
    query_tokens = set(query.split())

    def score(row):
        title_tokens = set(row["title_norm"].split())
        category_tokens = set(row["category_norm"].split())
        return len(query_tokens & title_tokens) + len(query_tokens & category_tokens)

    df = df.copy()
    df["score"] = df.apply(score, axis=1)

    best = df[df["score"] > 0].sort_values("score", ascending=False)

    return best.head(1)



def check_and_reserve(product_row, quantity):
    if product_row["stock"] >= quantity:
        product_row["stock"] -= quantity
        return True
    return False
