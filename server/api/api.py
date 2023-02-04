from typing import Literal

from pydantic import BaseModel
from starlite import OpenAPIConfig, Starlite, get


class OK(BaseModel):
    text: Literal["OK"] = "OK"


@get("/status")
def status() -> OK:
    return OK()


app = Starlite(
    route_handlers=[status],
    openapi_config=OpenAPIConfig(
        title="Gradwork API",
        version="1.0.0",
    ),
)
