#request → middleware → dependency → route → response
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import time
import logging


logger = logging.getLogger("middleware")


# =========================
# 1) Logging Middleware
# =========================
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """تسجيل كل الطلبات"""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        logger.info(f"📥 {request.method} {request.url.path}")

        response = await call_next(request)

        process_time = time.time() - start_time

        logger.info(f"📤 {response.status_code} - {process_time:.3f}s")

        response.headers["X-Process-Time"] = str(process_time)
        return response


# =========================
# 2) Rate Limiting Middleware (Simple In-Memory)
# =========================
class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limit بسيط لكل IP"""

    def __init__(self, app, calls_per_minute: int = 60):
        super().__init__(app)
        self.calls_per_minute = calls_per_minute
        self.requests = {}  # {ip: [timestamps]}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()

        # initialize
        if client_ip not in self.requests:
            self.requests[client_ip] = []

        # remove old requests (> 60 sec)
        self.requests[client_ip] = [
            t for t in self.requests[client_ip]
            if now - t < 60
        ]

        # check limit
        if len(self.requests[client_ip]) >= self.calls_per_minute:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Try again later."}
            )

        # add current request
        self.requests[client_ip].append(now)

        return await call_next(request)
