from typing import Any
from uuid import UUID

import httpx


class APIClientError(Exception):
    """Raised when the backend API request fails."""

    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


class APIClient:
    """HTTP client for communicating with the ChatGPT Clone backend."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"

        try:
            async with httpx.AsyncClient(
                timeout=self.timeout
            ) as client:
                response = await client.request(
                    method,
                    url,
                    **kwargs,
                )

        except httpx.TimeoutException as exc:
            raise APIClientError(
                "The backend request timed out."
            ) from exc

        except httpx.RequestError as exc:
            raise APIClientError(
                "Unable to connect to the backend."
            ) from exc

        if response.is_error:
            try:
                detail = response.json().get(
                    "detail",
                    "Backend request failed.",
                )
            except ValueError:
                detail = "Backend request failed."

            raise APIClientError(
                str(detail),
                status_code=response.status_code,
            )

        return response.json()

    async def create_conversation(
        self,
        title: str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {}

        if title:
            payload["title"] = title

        return await self._request(
            "POST",
            "/conversations",
            json=payload,
        )

    async def list_conversations(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        return await self._request(
            "GET",
            "/conversations",
            params={
                "limit": limit,
                "offset": offset,
            },
        )

    async def get_conversation(
        self,
        conversation_id: UUID | str,
    ) -> dict[str, Any]:
        return await self._request(
            "GET",
            f"/conversations/{conversation_id}",
        )

    async def list_messages(
        self,
        conversation_id: UUID | str,
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        return await self._request(
            "GET",
            f"/conversations/{conversation_id}/messages",
            params={
                "limit": limit,
                "offset": offset,
            },
        )

    async def send_chat_message(
        self,
        conversation_id: UUID | str,
        content: str,
    ) -> dict[str, Any]:
        return await self._request(
            "POST",
            f"/conversations/{conversation_id}/chat",
            json={
                "content": content,
            },
        )

    async def health_check(self) -> dict[str, Any]:
        return await self._request(
            "GET",
            "/health",
        )
