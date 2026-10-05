import logging
import time

from openai import (
    AsyncOpenAI,
    RateLimitError,
    AuthenticationError,
    APITimeoutError,
    APIConnectionError,
    APIStatusError,
)

from app.core.config import settings
from app.exceptions.custom_exceptions import AIProviderError


logger = logging.getLogger(__name__)


class AIService:

    MODEL = settings.GROQ_MODEL

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

    async def generate_response(self, messages: list[dict[str,str]]) -> str:
        try:
            start_time = time.perf_counter()

            logger.info(
                "Starting AI provider execution:  model=%s",
                self.MODEL
            )
            response = await self.client.responses.create(
                model=self.MODEL,
                input=messages,
                max_output_tokens=settings.CHAT_MAX_OUTPUT_TOKENS
            )

            output = response.output_text

            if not output:
                raise AIProviderError(
                    "AI provider returned an empty response."
                )

            duration = time.perf_counter() - start_time

            logger.info(
                "AI provider execution completed sucessfully: model=%s  duration=%s",
                self.MODEL,
                duration
            )
            return output

        except RateLimitError as exc:
            logger.error(
                "AI provider rate limit error: model=%s",
                self.MODEL
            )
            raise AIProviderError(
                "AI provider rate limit or quota exceeded.",
                status_code=429
            ) from exc

        except AuthenticationError as exc:
            logger.error(
                "AI provider authentication error: model=%s",
                self.MODEL
            )
            raise AIProviderError(
                "AI provider authentication failed.",
                status_code=502
            ) from exc

        except APITimeoutError as exc:
            logger.error(
                "AI provider timed out: model=%s",
                self.MODEL
            )
            raise AIProviderError(
                "AI provider request timed out.",
                status_code=504
            ) from exc

        except APIConnectionError as exc:
            logger.error(
                "AI provider connection error: model=%s",
                self.MODEL
            )
            raise AIProviderError(
                "unable to connect to AI provider.",
                status_code=503
            ) from exc

        except APIStatusError as exc:
            logger.error(
                "AI provider returned an API status error: model=%s",
                self.MODEL
            )
            raise AIProviderError(
                "AI provider request failed.",
                status_code=502
            ) from exc
