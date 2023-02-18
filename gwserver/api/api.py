from starlite import OpenAPIConfig, Router, Starlite

from . import controller

app = Starlite(
    route_handlers=[
        Router(path="/image", route_handlers=[controller.Image], tags=["Image"]),
        Router(path="/category", route_handlers=[controller.Category], tags=["Category"]),
    ],
    openapi_config=OpenAPIConfig(
        title="Gradwork API",
        version="1.0.0",
    ),
)
