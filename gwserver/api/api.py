from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig

from . import router

app = Litestar(
    cors_config=CORSConfig(),
    openapi_config=OpenAPIConfig(title="Gradwork API", version="1.0.0"),
    route_handlers=[
        router.image,
        router.category,
    ],
)
