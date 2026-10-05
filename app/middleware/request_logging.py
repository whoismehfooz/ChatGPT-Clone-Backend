import logging
import time

from fastapi import Request


logger = logging.getLogger("app.middleware.request_logging")


async def request_logging_middleware(
    request: Request,
    call_next,
):
    start_time = time.perf_counter()

    logger.info(
        "Request started: method=%s path=%s",
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)

    except Exception:
        duration = time.perf_counter() - start_time

        logger.exception(
            "Request failed: method=%s path=%s duration=%.3fs",
            request.method,
            request.url.path,
            duration,
        )

        raise

    duration = time.perf_counter() - start_time

    logger.info(
        "Request completed: method=%s path=%s status=%s duration=%.3fs",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    return response
