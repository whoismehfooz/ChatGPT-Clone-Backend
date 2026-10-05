from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.dependencies import get_ai_service
from app.main import app
from tests.fakes.integration_ai_service import IntegrationAIService


@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_chat_flow_with_real_database():
    app.dependency_overrides[get_ai_service] = IntegrationAIService

    try:
        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:

            create_response = await client.post(
                "/conversations",
                json={"title": "Integration Test Conversation"},
            )

            assert create_response.status_code == 201

            conversation = create_response.json()
            conversation_id = conversation["id"]

            assert UUID(conversation_id)
            assert conversation["title"] == "Integration Test Conversation"

            chat_response = await client.post(
                f"/conversations/{conversation_id}/chat",
                json={"content": "Hello integration database"},
            )

            assert chat_response.status_code == 200

            chat_data = chat_response.json()

            assert chat_data["conversation_id"] == conversation_id
            assert chat_data["content"] == "integration assistant response"

            messages_response = await client.get(
                f"/conversations/{conversation_id}/messages",
            )

            assert messages_response.status_code == 200

            messages = messages_response.json()["items"]

            assert len(messages) == 2

            assert messages[0]["role"] == "user"
            assert messages[0]["content"] == "Hello integration database"

            assert messages[1]["role"] == "assistant"
            assert messages[1]["content"] == "integration assistant response"

            conversation_response = await client.get(
                f"/conversations/{conversation_id}",
            )

            assert conversation_response.status_code == 200

            persisted_conversation = conversation_response.json()

            assert persisted_conversation["id"] == conversation_id
            assert persisted_conversation["title"] == (
                "Integration Test Conversation"
            )

    finally:
        app.dependency_overrides.clear()
