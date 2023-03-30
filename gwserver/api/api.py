from starlite import OpenAPIConfig, Router, Starlite

from gwserver.core import config

from . import controller

app = Starlite(
    route_handlers=[
        Router(
            path=f"{config.API_ROOT_PATH}/image",
            route_handlers=[controller.Image],
            tags=["Image"],
        ),
        Router(
            path=f"{config.API_ROOT_PATH}/category",
            route_handlers=[controller.Category],
            tags=["Category"],
        ),
    ],
    openapi_config=OpenAPIConfig(
        title="Gradwork API",
        version="1.0.0",
    ),
)
