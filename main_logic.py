from speech.asr import transcribe
from nlp.parser import parse_command
from inventory.store import find_product
from orders.service import process_order


def handle_voice_command(audio_bytes, products, order_history, logger=None):

    if logger:
        logger("🧠 Transcribing audio...")

    text = transcribe(audio_bytes)

    if logger:
        logger(f"📝 Recognized Text: {text}")

    if not text:
        return "I didn't hear anything."

    if text.lower() in ["stop", "quit", "exit"]:
        return "Goodbye."

    intent, product_name, quantity = parse_command(text)

    if logger:
        logger(f"⚙ Intent: {intent}, Product: {product_name}, Qty: {quantity}")

    if intent == "ORDER":
        product = find_product(product_name, products)

        if product is None or product.empty:
            return "Sorry, that product is not available."

        success, response = process_order(product, quantity, order_history)

        if logger:
            logger("✅ Order processed")

        return response

    elif intent == "HISTORY":
        if order_history.is_empty():
            return "You have not placed any orders yet."
        else:
            last = order_history.get_all_orders()[-1]
            return f"You last ordered {last['quantity']} {last['product_name']}."

    else:
        return "Sorry, I did not understand your request."
