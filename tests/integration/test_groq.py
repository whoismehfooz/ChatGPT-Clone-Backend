import pytest

from app.services.ai_service import AIService


@pytest.mark.integration
@pytest.mark.asyncio
async def test_groq_real_response():
    service = AIService()

    response = await service.generate_response(
        [
            {
                "role": "user",
                "content": (
                    "Reply with exactly: "
                    "integration test passed"
                ),
            }
        ]
    )

    assert response
    assert isinstance(response, str)

    assert "integration test passed" in response.lower()
