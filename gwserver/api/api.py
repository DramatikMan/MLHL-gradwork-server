from starlite import OpenAPIConfig, Router, Starlite
from starlite.config.cors import CORSConfig

from gwserver.core import config

from . import view

app = Starlite(
    cors_config=CORSConfig(),
    openapi_config=OpenAPIConfig(
        title="Gradwork API",
        version="1.0.0",
    ),
    route_handlers=[
        Router(
            path=f"{config.API_ROOT_PATH}/image",
            route_handlers=[view.Image],
            tags=["Image"],
        ),
        Router(
            path=f"{config.API_ROOT_PATH}/category",
            route_handlers=[view.Category],
            tags=["Category"],
        ),
    ],
)
