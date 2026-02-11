# nlp/parser.py
import re

NUMBER_MAP = {
    "one": 1, "two": 2, "three": 3,
    "four": 4, "five": 5
}

STOP_WORDS = {
    "order", "buy", "please", "a", "an", "the"
}

def parse_command(text: str):
    # Normalize
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)

    intent = "UNKNOWN"
    quantity = 1

    tokens = text.split()

    # Intent
    if "order" in tokens or "buy" in tokens:
        intent = "ORDER"

    # Quantity: numeric
    for t in tokens:
        if t.isdigit():
            quantity = int(t)
            break

    # Quantity: word-based (fallback)
    for word, num in NUMBER_MAP.items():
        if word in tokens:
            quantity = num
            break

    # Product tokens (remove stopwords, numbers)
    product_tokens = [
        t for t in tokens
        if t not in STOP_WORDS
        and not t.isdigit()
        and t not in NUMBER_MAP
    ]

    product = " ".join(product_tokens)

    return intent, product.strip(), quantity
