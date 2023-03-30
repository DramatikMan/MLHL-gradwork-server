from starlite import OpenAPIConfig, Response, Router, Starlite, asgi
from starlite.types import Receive, Scope, Send

from gwserver.core import config

from . import controller


@asgi(config.API_ROOT_PATH, is_mount=True)
async def root_path_handler(scope: Scope, receive: Receive, send: Send) -> None:
    response = Response(content={"forwarded_path": scope["path"]})
    await response(scope, receive, send)


app = Starlite(
    route_handlers=[
        root_path_handler,
        Router(path="/image", route_handlers=[controller.Image], tags=["Image"]),
        Router(path="/category", route_handlers=[controller.Category], tags=["Category"]),
    ],
    openapi_config=OpenAPIConfig(
        title="Gradwork API",
        version="1.0.0",
    ),
)
