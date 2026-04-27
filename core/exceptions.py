# core/errors.py

import time
import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# =========================
# Logger Setup
# =========================
logger = logging.getLogger("app")
logging.basicConfig(level=logging.INFO)


# =========================
# Error Codes
# =========================
class ErrorCodes:
    USER_NOT_FOUND = "USR_404_01"
    INVALID_TOKEN = "AUTH_401_01"
    UNAUTHORIZED = "AUTH_403_01"

    NODE_NOT_FOUND = "GRAPH_404_01"
    EDGE_NOT_FOUND = "GRAPH_404_02"
    PATH_NOT_FOUND = "GRAPH_404_03"

    INVALID_GRAPH = "GRAPH_400_01"

    ALGORITHM_ERROR = "ALG_400_01"
    NO_SOLUTION = "ALG_404_01"

    DATABASE_ERROR = "DB_500_01"
    FILE_ERROR = "FILE_500_01"

    INTERNAL_ERROR = "SYS_500_00"


# =========================
# Base Exception
# =========================
class SmartCityException(Exception):
    def __init__(self, message: str, status_code: int = 500, code: str = "UNKNOWN", details: dict = None):
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details or {}
        super().__init__(message)


# =========================
# Custom Exceptions
# =========================
class UserNotFoundError(SmartCityException):
    def __init__(self, user_id: str = None):
        super().__init__(
            message=f"User {user_id} not found" if user_id else "User not found",
            status_code=404,
            code=ErrorCodes.USER_NOT_FOUND,
            details={"user_id": user_id}
        )


class InvalidTokenError(SmartCityException):
    def __init__(self):
        super().__init__("Invalid or expired token", 401, ErrorCodes.INVALID_TOKEN)


class UnauthorizedError(SmartCityException):
    def __init__(self):
        super().__init__("Unauthorized access", 403, ErrorCodes.UNAUTHORIZED)


class NodeNotFoundError(SmartCityException):
    def __init__(self, node_id: str):
        super().__init__(
            f"Node '{node_id}' not found",
            404,
            ErrorCodes.NODE_NOT_FOUND,
            {"node_id": node_id}
        )


class EdgeNotFoundError(SmartCityException):
    def __init__(self, edge_id: str):
        super().__init__(
            f"Edge '{edge_id}' not found",
            404,
            ErrorCodes.EDGE_NOT_FOUND,
            {"edge_id": edge_id}
        )


class PathNotFoundError(SmartCityException):
    def __init__(self, start: str, end: str):
        super().__init__(
            f"No path from '{start}' to '{end}'",
            404,
            ErrorCodes.PATH_NOT_FOUND,
            {"start": start, "end": end}
        )


class InvalidGraphError(SmartCityException):
    def __init__(self, reason: str):
        super().__init__(
            f"Invalid graph: {reason}",
            400,
            ErrorCodes.INVALID_GRAPH,
            {"reason": reason}
        )


class AlgorithmError(SmartCityException):
    def __init__(self, algorithm: str, reason: str):
        super().__init__(
            f"Algorithm '{algorithm}' failed: {reason}",
            400,
            ErrorCodes.ALGORITHM_ERROR,
            {"algorithm": algorithm, "reason": reason}
        )

class ProjectNotFoundError(SmartCityException):
    def __init__(self, project_name: str):
        super().__init__(
            f"Project '{project_name}' not found",
            404,
            "PROJECT_404_01",
            {"project_name": project_name}
        )
class NoSolutionError(SmartCityException):
    def __init__(self, problem: str):
        super().__init__(
            f"No solution for {problem}",
            404,
            ErrorCodes.NO_SOLUTION,
            {"problem": problem}
        )


class DatabaseError(SmartCityException):
    def __init__(self, operation: str, detail: str):
        super().__init__(
            f"DB error on {operation}: {detail}",
            500,
            ErrorCodes.DATABASE_ERROR,
            {"operation": operation, "detail": detail}
        )
class VehicleNotFoundError(SmartCityException):
    def __init__(self, vehicle_id: str = None):
        super().__init__(
            message=f"Vehicle {vehicle_id} not found" if vehicle_id else "Vehicle not found",
            status_code=404,
            code="VEHICLE_404_01",
            details={"vehicle_id": vehicle_id}
        )

class FileOperationError(SmartCityException):
    def __init__(self, filename: str, operation: str, error: str):
        super().__init__(
            f"Cannot {operation} '{filename}': {error}",
            500,
            ErrorCodes.FILE_ERROR,
            {"filename": filename, "operation": operation}
        )


# =========================
# Exception Handlers
# =========================
async def smart_city_exception_handler(request: Request, exc: SmartCityException):
    logger.warning(f"{exc.code} | {exc.message} | {exc.details}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message,
            "code": exc.code,
            "details": exc.details
        }
    )


async def global_exception_handler(request: Request, exc: Exception):
    logger.error("UNHANDLED ERROR", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "code": ErrorCodes.INTERNAL_ERROR
        }
    )


# =========================
# Middleware (Logging + Safety)
# =========================
class ErrorHandlingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start = time.time()

        try:
            response = await call_next(request)

            process_time = time.time() - start
            logger.info(f"{request.method} {request.url} | {response.status_code} | {process_time:.3f}s")

            return response

        except Exception as e:
            logger.error("Middleware caught error", exc_info=True)

            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "Unexpected server error",
                    "code": ErrorCodes.INTERNAL_ERROR
                }
            )


# =========================
# FastAPI Setup Helper
# =========================
def setup_error_handling(app: FastAPI):
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_exception_handler(SmartCityException, smart_city_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)