import asyncio

import streamlit as st

from ui.api_client import APIClient, APIClientError
from ui.components.chat import (
    render_backend_error,
    render_empty_conversation,
    render_message,
)
from ui.config import BACKEND_URL


api_client = APIClient(
    base_url=BACKEND_URL,
)


st.set_page_config(
    page_title="ChatGPT Clone",
    page_icon="💬",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }

    section[data-testid="stSidebar"] {
        width: 280px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if "active_conversation_id" not in st.session_state:
    st.session_state["active_conversation_id"] = None


def run_async(coroutine):
    return asyncio.run(coroutine)


def load_conversations() -> list[dict]:
    response = run_async(
        api_client.list_conversations()
    )

    return response["items"]


def load_messages(
    conversation_id: str,
) -> list[dict]:
    response = run_async(
        api_client.list_messages(
            conversation_id
        )
    )

    return response["items"]


st.title("💬 ChatGPT Clone")

st.caption(
    "Stateful AI conversations powered by FastAPI, "
    "PostgreSQL, and Groq."
)


st.sidebar.title("Conversations")

try:
    health = run_async(
        api_client.health_check()
    )

    st.sidebar.success(
        f"Backend: {health['status']}"
    )

except APIClientError:
    st.sidebar.error(
        "Backend: unavailable"
    )

try:
    conversations = load_conversations()

except APIClientError as exc:
    conversations = []
    render_backend_error(str(exc))


if st.sidebar.button(
    "＋ New Conversation",
    use_container_width=True,
):
    try:
        conversation = run_async(
            api_client.create_conversation()
        )

        st.session_state["active_conversation_id"] = (
            conversation["id"]
        )

        st.rerun()

    except APIClientError as exc:
        st.sidebar.error(
            f"Unable to create conversation: {exc}"
        )


if conversations:
    conversation_options = {
        conversation["title"]
        or f"Conversation {conversation['id'][:8]}":
        conversation["id"]
        for conversation in conversations
    }

    conversation_ids = list(
        conversation_options.values()
    )

    active_conversation_id = st.session_state.get(
        "active_conversation_id"
    )

    if active_conversation_id not in conversation_ids:
        active_conversation_id = conversation_ids[0]

        st.session_state["active_conversation_id"] = (
            active_conversation_id
        )

    selected_title = st.sidebar.selectbox(
        "Select conversation",
        options=list(conversation_options.keys()),
        index=conversation_ids.index(
            active_conversation_id
        ),
    )

    selected_conversation_id = conversation_options[
        selected_title
    ]

    if (
        selected_conversation_id
        != st.session_state["active_conversation_id"]
    ):
        st.session_state["active_conversation_id"] = (
            selected_conversation_id
        )

        st.rerun()

else:
    st.sidebar.info(
        "No conversations yet."
    )

    st.session_state["active_conversation_id"] = None


st.divider()


active_conversation_id = st.session_state.get(
    "active_conversation_id"
)


if not active_conversation_id:
    st.subheader("Start a new conversation")

    st.write(
        "Create a conversation from the sidebar, "
        "then send a message to start chatting."
    )

else:
    selected_conversation = next(
        (
            conversation
            for conversation in conversations
            if conversation["id"] == active_conversation_id
        ),
        None,
    )

    if selected_conversation:
        conversation_title = (
            selected_conversation["title"]
            or f"Conversation {active_conversation_id[:8]}"
        )

        st.subheader(conversation_title)

    try:
        messages = load_messages(
            active_conversation_id
        )

    except APIClientError as exc:
        render_backend_error(str(exc))
        messages = []


    if messages:
        for message in messages:
            render_message(message)

    else:
        render_empty_conversation()


    prompt = st.chat_input(
        "Message the assistant..."
    )


    if prompt:
        try:
            with st.spinner("Thinking..."):
                run_async(
                    api_client.send_chat_message(
                        conversation_id=active_conversation_id,
                        content=prompt,
                    )
                )

            st.rerun()

        except APIClientError as exc:
            st.error(
                f"Unable to send message: {exc}"
            )
