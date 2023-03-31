from starlite import OpenAPIConfig, Router, Starlite
from starlite.config.cors import CORSConfig

from gwserver.core import config

from . import controller

app = Starlite(
    cors_config=CORSConfig(),
    openapi_config=OpenAPIConfig(
        title="Gradwork API",
        version="1.0.0",
    ),
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
)
