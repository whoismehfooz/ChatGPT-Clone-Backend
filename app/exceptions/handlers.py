from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    ConversationNotFoundError,
    AIProviderError,
    ContextBudgetExceededError
)


def register_exeption_handlers(app:FastAPI):
    @app.exception_handler(ConversationNotFoundError)
    async def conversation_not_found_handler(
        request: Request,
        exc: ConversationNotFoundError
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail":str(exc)
            }
        )



    @app.exception_handler(AIProviderError)
    async def ai_provider_error_handler(
        request: Request,
        exc: AIProviderError
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail":str(exc)
            }
        )

    @app.exception_handler(ContextBudgetExceededError)
    async def context_budget_error_handler(
        request: Request ,
        exc: ContextBudgetExceededError
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail":str(exc)
            }
        )
