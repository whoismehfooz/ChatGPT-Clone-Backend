from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db_session
from app.core.config import settings

from app.services.ai_service import AIService
from app.services.chat_service import ChatService
from app.services.context_builder import ContextBuilder
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService
from app.services.token_counter import TokenCounter


def get_ai_service() -> AIService:
    return AIService()


def get_chat_service(
    db_session: AsyncSession = Depends(get_db_session),
    ai_service: AIService = Depends(get_ai_service),
) -> ChatService:
    conversation_service = ConversationService(db_session)
    message_service = MessageService(db_session)

    token_counter = TokenCounter()

    context_builder = ContextBuilder(
        token_counter=token_counter,
        context_token_budget=settings.CHAT_CONTEXT_TOKEN_BUDGET,
        system_prompt=settings.CHAT_SYSTEM_PROMPT,
    )

    return ChatService(
        conversation_service=conversation_service,
        message_service=message_service,
        context_builder=context_builder,
        ai_service=ai_service,
    )
