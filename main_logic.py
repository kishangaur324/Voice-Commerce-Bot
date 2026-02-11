from audio.recorder import record_until_silence
from speech.asr import transcribe
from audio.tts import speak
from nlp.parser import parse_command
from inventory.store import find_product
from orders.service import process_order


def handle_voice_command(products, order_history):
    print("Listening...")
    audio = record_until_silence()

    print("Processing...")
    text = transcribe(audio)

    print("You said:", text)

    if not text:
        return "I didn't hear anything."

    if text.lower() in ["stop", "quit", "exit"]:
        speak("Goodbye.")
        return "Goodbye."

    intent, product_name, quantity = parse_command(text)

    print("intent:", intent, "product:", product_name, "quantity:", quantity)

    if intent == "ORDER":
        product = find_product(product_name, products)

        if product is None or product.empty:
            response = "Sorry, that product is not available."
            speak(response)
            return response

        success, response = process_order(product, quantity, order_history)
        speak(response)
        return response

    elif intent == "HISTORY":
        if order_history.is_empty():
            response = "You have not placed any orders yet."
        else:
            last = order_history.get_all_orders()[-1]
            response = f"You last ordered {last['quantity']} {last['product_name']}."

        speak(response)
        return response

    else:
        response = "Sorry, I did not understand your request."
        speak(response)
        return response
