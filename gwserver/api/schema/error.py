from typing import Literal

from pydantic import BaseModel
from starlite import status_codes


class NOT_FOUND(BaseModel):
    status_code: Literal[404] = status_codes.HTTP_404_NOT_FOUND
    detail: str = "Not found."
