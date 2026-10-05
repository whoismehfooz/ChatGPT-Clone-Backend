from uuid import UUID

from app.services.ai_service import AIService
from app.services.context_builder import ContextBuilder
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService

from app.schemas.chat import ChatResponse
from app.exceptions.custom_exceptions import ConversationNotFoundError


class ChatService:

    def __init__(
        self,
        conversation_service: ConversationService,
        message_service: MessageService,
        context_builder: ContextBuilder,
        ai_service: AIService,
    ):
        self.conversation_service = conversation_service
        self.message_service = message_service
        self.context_builder = context_builder
        self.ai_service = ai_service

    async def send_message(
        self,
        conversation_id: UUID,
        content: str
    ) -> ChatResponse:

        conversation = await self.conversation_service.get_conversation(
            conversation_id
        )

        if conversation is None:
            raise ConversationNotFoundError(
                "Conversation not found.",
                status_code=404
            )

        user_message = await self.message_service.create_message(
            conversation_id=conversation_id,
            role="user",
            content=content
        )

        messages = await self.message_service.list_recent_messages(
            conversation_id=conversation_id,
            limit=100
        )

        context = self.context_builder.build(messages)

        assistant_content = await self.ai_service.generate_response(
            context
        )

        assistant_message = await self.message_service.create_message(
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_content
        )

        return ChatResponse(
            conversation_id=conversation_id,
            user_message_id=user_message.id,
            assistant_message_id=assistant_message.id,
            content=assistant_message.content
        )
