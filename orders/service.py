def process_order(product_df, quantity, history):
    if product_df.empty:
        return False, "Sorry, that product is not available right now."

    product = product_df.iloc[0]

    history.add_order(
        product_name=product["title"],
        quantity=quantity,
        price=product["price"]
    )

    return True, f"Your order for {quantity} {product['title']} has been placed."
