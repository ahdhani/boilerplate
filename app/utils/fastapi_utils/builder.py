from __future__ import annotations

from collections.abc import Sequence
from logging import Logger
from typing import Any, TypeVar

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.fastapi_utils.exception import ExceptionBase

# Type variable for middleware
MiddlewareType = TypeVar("MiddlewareType", bound=BaseHTTPMiddleware)


class FastApiBuilder:
    """A builder class for configuring and customizing a FastAPI application.

    This class provides a fluent interface for setting up common FastAPI configurations,
    middleware, exception handlers, and routes in a clean and maintainable way.

    Attributes:
        app: The FastAPI application instance.
        env: Current environment (e.g., "DEV", "PROD").
        logger: Logger instance for application logging.
    """

    def __init__(
        self,
        title: str,
        version: str,
        logger: Logger,
        hide_docs: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize the FastAPI builder.

        Args:
            title: The title of the FastAPI application.
            version: The version of the API.
            logger: Configured logger instance for application logging.
            env: Current environment (e.g., "DEV", "PROD", "TEST").
            **kwargs: Additional keyword arguments passed to FastAPI constructor.
        """
        self.app = FastAPI(
            title=title,
            version=version,
            docs_url="/docs" if hide_docs is False else None,
            redoc_url="/redoc" if hide_docs is False else None,
            openapi_url="/openapi.json" if hide_docs is False else None,
            **kwargs,
        )
        self.logger = logger

    def handle_exceptions(self) -> FastApiBuilder:
        """Configure global exception handlers for the application.

        Handles:
        - Custom application exceptions (ExceptionBase)
        - Request validation errors
        - Pydantic validation errors
        - General server errors (500)
        - HTTP exceptions

        Returns:
            Self for method chaining.
        """

        @self.app.exception_handler(ExceptionBase)
        async def handle_custom_exceptions(
            _: Request, exc: ExceptionBase
        ) -> JSONResponse:
            """Handle custom application exceptions."""
            self.logger.exception(
                "Custom exception occurred",
                extra={"status_code": exc.status_code, "detail": exc.detail},
            )
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "exception": exc.__class__.__name__,
                    "detail": exc.detail,
                    # "error_code": getattr(exc, "error_code", None),
                },
            )

        @self.app.exception_handler(RequestValidationError)
        async def handle_validation_errors(
            _: Request, exc: RequestValidationError
        ) -> JSONResponse:
            """Handle request validation errors."""
            self.logger.warning(
                "Request validation error",
                extra={"errors": exc.errors(), "body": exc.body},
            )
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "exception": exc.__class__.__name__,
                    "detail": exc.errors(),
                },
            )

        @self.app.exception_handler(ValidationError)
        async def handle_pydantic_validation_errors(
            _: Request, exc: ValidationError
        ) -> JSONResponse:
            """Handle Pydantic validation errors."""
            self.logger.warning(
                "Pydantic validation error", extra={"errors": exc.errors()}
            )
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "exception": exc.__class__.__name__,
                    "detail": exc.errors(),
                },
            )

        @self.app.exception_handler(HTTPException)
        async def handle_http_exceptions(
            _: Request, exc: HTTPException
        ) -> JSONResponse:
            """Handle HTTP exceptions."""
            if exc.status_code >= 500:
                self.logger.error(
                    "Server error occurred",
                    extra={"status_code": exc.status_code, "detail": exc.detail},
                )
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "exception": exc.__class__.__name__,
                    "detail": exc.detail,
                },
            )

        @self.app.exception_handler(Exception)
        async def handle_generic_exception(_: Request, exc: Exception) -> JSONResponse:
            """Handle all other uncaught exceptions."""
            self.logger.exception(f"Unhandled exception occurred: {str(exc)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "exception": "InternalServerError",
                    "detail": "Internal Server Error",
                },
            )

        return self

    def add_health_endpoint(self, path: str = "/health") -> FastApiBuilder:
        """Add a health check endpoint to the application.

        Args:
            path: The URL path for the health check endpoint.

        Returns:
            Self for method chaining.
        """

        @self.app.get(path, status_code=status.HTTP_200_OK, tags=["health"])
        async def health_check() -> dict[str, str]:
            """Health check endpoint."""
            return {"status": "success"}

        return self

    def add_cors_middleware(
        self,
        origins: Sequence[str],
        allow_credentials: bool = True,
        allow_methods: Sequence[str] = (
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "OPTIONS",
        ),
        allow_headers: Sequence[str] = ("*",),
        expose_headers: Sequence[str] = ("*",),
        max_age: int = 600,
    ) -> FastApiBuilder:
        """Add CORS middleware to the application.

        Args:
            origins: List of allowed origins. Use ["*"] to allow all origins.
            allow_credentials: Whether to support credentials in CORS requests.
            allow_methods: List of allowed HTTP methods.
            allow_headers: List of allowed request headers.
            expose_headers: List of exposed response headers.
            max_age: Maximum time in seconds to cache CORS preflight responses.

        Returns:
            Self for method chaining.
        """
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in origins],
            allow_credentials=allow_credentials,
            allow_methods=list(allow_methods),
            allow_headers=list(allow_headers),
            expose_headers=list(expose_headers),
            max_age=max_age,
        )
        return self

    def add_root_router(
        self, router: Any, prefix: str = "/api/v1", **kwargs: Any
    ) -> FastApiBuilder:
        """Include a router with the given prefix.

        Args:
            router: The router to include.
            prefix: The prefix to add to all routes in the router.
            **kwargs: Additional arguments to pass to include_router.

        Returns:
            Self for method chaining.
        """
        self.app.include_router(router, prefix=prefix, **kwargs)
        return self

    def build(self) -> FastAPI:
        """Build and return the configured FastAPI application.

        Returns:
            The configured FastAPI application instance.
        """
        return self.app
