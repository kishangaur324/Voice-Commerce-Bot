import streamlit as st
import base64
import uuid
from inventory.loader import load_products
from history.orders import OrderHistory
from main_logic import handle_voice_command
from speech.tts import generate_speech
from speech.asr import transcribe  # to show transcript before logic

st.set_page_config(page_title="Voice Commerce Assistant", layout="centered")
st.title("🎙️ Voice Commerce Assistant")

# ---------------------------
# Initialize session state
# ---------------------------
if "order_history" not in st.session_state:
    st.session_state.order_history = OrderHistory()
    st.session_state.products = load_products("data/amazon_products.csv")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.write("Click record and speak your command.")

# ---------------------------
# 🎤 Browser Microphone Input
# ---------------------------
audio_file = st.audio_input("Record your voice")

if audio_file is not None:

    log_placeholder = st.empty()

    def logger(msg):
        log_placeholder.markdown(f"**{msg}**")

    logger("🎤 Audio received.")
    logger("🧠 Transcribing audio...")

    audio_bytes = audio_file.read()

    # 🔹 Get transcript first (so we can show user message)
    user_text = transcribe(audio_bytes)

    logger(f"📝 You said: {user_text}")

    if not user_text:
        response = "I didn't hear anything."
    else:
        # 🔹 Process command
        response = handle_voice_command(
            audio_bytes,
            st.session_state.products,
            st.session_state.order_history,
            logger=logger,
        )

    logger("🎉 Processing complete.")

    # ---------------------------
    # Store conversation
    # ---------------------------
    if user_text:
        st.session_state.chat_history.append(("User", user_text))

    st.session_state.chat_history.append(("Assistant", response))

    # ---------------------------
    # 🔊 Generate Speech
    # ---------------------------
    audio_bytes = generate_speech(response)

    st.audio(
        audio_bytes,
        format="audio/mp3",
        autoplay=True
    )

# ---------------------------
# Conversation History
# ---------------------------
st.subheader("Conversation History")

for sender, message in st.session_state.chat_history:
    if sender == "User":
        st.markdown(f"🧑 **You:** {message}")
    else:
        st.markdown(f"🤖 **Assistant:** {message}")
