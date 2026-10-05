from fastapi import FastAPI

from app.core.config import settings
from app.api.conversation import conversation_router
from app.api.message import message_router
from app.api.chat import chat_router
from app.exceptions.handlers import register_exeption_handlers
from app.middleware.request_logging import request_logging_middleware
from app.core.logging_config import configure_logging



app = FastAPI(
    title=settings.APP_NAME,
    description="This is a Backend learning project. Build by MEHFOOZ..",
    version="v1.0.0",
    contact={
        "name":"Mehfooz",
        "email":"mehfooz.sde@gmail.com"
    },
    license_info={
        "name":"MIT"
    },
    debug=settings.DEBUG
)


configure_logging()
app.include_router(conversation_router)
app.include_router(message_router)
app.include_router(chat_router)
app.middleware("http")(request_logging_middleware)
register_exeption_handlers(app)


@app.get('/health')

async def health_check():

    return {
        "status":"healthy",
        "service":settings.APP_NAME,
        "environment":settings.APP_ENV,
        "version":app.version
    }
