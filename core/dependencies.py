import time
import asyncio
import inspect
from functools import wraps
from typing import Callable, Any, Dict, Tuple


# =========================
# 1) Execution Time Logger (FIXED)
# =========================
def log_execution_time(func: Callable):
    """
    يدعم async + sync بدون كسر
    """

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        print(f"⏱️ {func.__name__} took {duration:.3f}s")
        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"⏱️ {func.__name__} took {duration:.3f}s")
        return result

    return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper


# =========================
# 2) In-Memory Cache (FIXED + SAFE)
# =========================
def require_cache(ttl: int = 60):
    """
    Cache بسيط + TTL + يدعم async/sync
    ⚠️ مناسب للتجارب فقط وليس distributed systems
    """

    cache: Dict[str, Tuple[Any, float]] = {}

    def make_key(func_name: str, args: tuple, kwargs: dict):
        return (
            func_name,
            str(args),
            tuple(sorted(kwargs.items()))
        )

    def decorator(func: Callable):

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            key = make_key(func.__name__, args, kwargs)

            # check cache
            if key in cache:
                value, timestamp = cache[key]
                if time.time() - timestamp < ttl:
                    return value

            result = await func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            key = make_key(func.__name__, args, kwargs)

            if key in cache:
                value, timestamp = cache[key]
                if time.time() - timestamp < ttl:
                    return value

            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result

        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

    return decorator