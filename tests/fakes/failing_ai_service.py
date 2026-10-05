from app.exceptions.custom_exceptions import AIProviderError


class FailingAIService:
    async def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        raise AIProviderError(
            "AI provider request failed.",
            status_code=502,
        )
