from uuid import uuid4

import pytest

from app.models import Conversation, Message
from app.services.chat_service import ChatService
from app.exceptions.custom_exceptions import ConversationNotFoundError

class FakeConversationService:
    def __init__(self,conversation):
        self.conversation = conversation

    async def get_conversation(self, conversation_id):
        return self.conversation


class FakeMessageService:
    def __init__(self, messages, user_message, assistant_message):
        self.messages = messages
        self.user_message = user_message
        self.assistant_message = assistant_message
        self.created_messages = []


    async def create_message(
            self,
            conversation_id,
            role,
            content
    ):
        message = (
            self.user_message
            if role == "user"
            else self.assistant_message
        )

        self.created_messages.append(
            {
                "conversation_id":conversation_id,
                "role":role,
                "content":content
            }
        )

        return message

    async def list_recent_messages(
            self,
            conversation_id,
            limit,
    ):
        return self.messages


class FakeContextBuilder:
    def __init__(self):
        self.recieved_messages = None

    def build(self,messages):
        self.recieved_messages = messages

        return [
            {
                "role":message.role,
                "content":message.content
            }
            for message in messages
        ]



class FakeAIService:
    def __init__(self):
        self.recieved_context = None

    async def generate_response(self, messages):
        self.recieved_context = messages

        return "Fake assistant response"



@pytest.mark.asyncio
async def test_send_message_happy_path():

    conversation_id = uuid4()

    conversation = Conversation(
        id=conversation_id,
        title="Test Conversation"
    )

    user_message = Message(
        id=uuid4(),
        conversation_id=conversation_id,
        role="user",
        content="Hello"
    )

    assistant_message = Message(
        id=uuid4(),
        conversation_id=conversation_id,
        role="assistant",
        content="Fake assistant response"
    )

    conversation_service = FakeConversationService(
        conversation
    )

    message_service = FakeMessageService(
        messages=[user_message],
        user_message=user_message,
        assistant_message=assistant_message
    )

    context_builder = FakeContextBuilder()
    ai_service = FakeAIService()

    chat_service = ChatService(
        conversation_service=conversation_service,
        message_service=message_service,
        context_builder=context_builder,
        ai_service=ai_service
    )

    response = await chat_service.send_message(
        conversation_id=conversation_id,
        content="Hello"
    )

    assert response.conversation_id == conversation_id
    assert response.user_message_id == user_message.id
    assert response.assistant_message_id == assistant_message.id
    assert response.content == "Fake assistant response"

    assert len(message_service.created_messages) == 2

    assert message_service.created_messages[0]["role"] == "user"
    assert message_service.created_messages[0]["content"] == "Hello"

    assert message_service.created_messages[1]["role"] == "assistant"
    assert message_service.created_messages[1]["content"] == "Fake assistant response"

    assert context_builder.recieved_messages == [user_message]

    assert ai_service.recieved_context == [
        {
            "role":"user",
            "content":"Hello"
        }
    ]


class MissingConversationService:

    async def get_conversation(self, conversation_id):
        return None


@pytest.mark.asyncio
async def test_send_message_conversation_not_found():

    chat_service = ChatService(
        conversation_service=MissingConversationService(),
        message_service=FakeMessageService(
            messages=[],
            user_message=None,
            assistant_message=None,
        ),
        context_builder=FakeContextBuilder(),
        ai_service=FakeAIService(),
    )

    with pytest.raises(
        ConversationNotFoundError,
        match="Conversation not found.",
    ):
        await chat_service.send_message(
            conversation_id=uuid4(),
            content="Hello",
        )
