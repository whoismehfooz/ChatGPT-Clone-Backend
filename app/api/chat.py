from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.api.dependencies import get_chat_service


chat_router = APIRouter(
    prefix="/conversations",
    tags=["Chat"]
)


@chat_router.post("/{conversation_id}/chat",response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def send_chat_message(
    conversation_id: UUID,
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
)->ChatResponse:
    return await chat_service.send_message(
        conversation_id=conversation_id,
        content=request.content
    )
