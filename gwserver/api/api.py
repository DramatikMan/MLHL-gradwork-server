from typing import Any, TypedDict

from litestar import Litestar, Response, status_codes
from litestar.config.cors import CORSConfig
from litestar.exceptions import HTTPException
from litestar.openapi import OpenAPIConfig

from . import router


class APIException(TypedDict):
    detail: str
    extra: dict[str, Any] | list[Any] | None


def exception_handler(_: Any, ex: Exception) -> Response[APIException]:
    if isinstance(ex, HTTPException):
        return Response(
            content=APIException(detail=ex.detail, extra=ex.extra),
            status_code=ex.status_code,
        )

    return Response(
        content=APIException(detail=str(ex), extra=None),
        status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
    )


app = Litestar(
    cors_config=CORSConfig(),
    openapi_config=OpenAPIConfig(title="Gradwork API", version="1.0.0"),
    route_handlers=[
        router.image,
        router.category,
    ],
    exception_handlers={
        Exception: exception_handler,
    },
)
