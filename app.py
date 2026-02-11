import streamlit as st
from inventory.loader import load_products
from history.orders import OrderHistory
from main_logic import handle_voice_command

# Page config
st.set_page_config(page_title="Voice Commerce Assistant", layout="centered")

st.title("🎙️ Voice Commerce Assistant")

# Initialize session state
if "order_history" not in st.session_state:
    st.session_state.order_history = OrderHistory()
    st.session_state.products = load_products("data/amazon_products.csv")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Buttons
col1, col2 = st.columns(2)

with col1:
    start = st.button("🎤 Start Listening")

with col2:
    stop = st.button("⏹ Stop")

# Start listening
if start:
    with st.spinner("Listening and processing..."):
        response = handle_voice_command(
            st.session_state.products,
            st.session_state.order_history
        )

        st.session_state.chat_history.append(("Assistant", response))

# Stop
if stop:
    st.success("Assistant stopped.")

# Display chat history
st.subheader("Conversation History")

for sender, message in st.session_state.chat_history:
    if sender == "Assistant":
        st.markdown(f"🤖 **Assistant:** {message}")
