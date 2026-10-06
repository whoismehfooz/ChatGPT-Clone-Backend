import streamlit as st


def render_message(message: dict) -> None:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def render_empty_conversation() -> None:
    st.info(
        "No messages in this conversation yet. "
        "Send a message below to get started."
    )


def render_backend_error(message: str) -> None:
    st.error(
        f"Backend unavailable: {message}"
    )
