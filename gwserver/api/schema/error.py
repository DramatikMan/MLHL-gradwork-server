from typing import Literal, Type

from pydantic import BaseModel
from starlite import HTTPException, status_codes


def ApiException(error: Type[BaseModel]) -> HTTPException:
    return HTTPException(**error().dict())


class NOT_FOUND(BaseModel):
    status_code: Literal[404] = status_codes.HTTP_404_NOT_FOUND
    detail: str = "Not found."


class IMAGE_CHECK_FAILURE(BaseModel):
    status_code: Literal[422] = status_codes.HTTP_422_UNPROCESSABLE_ENTITY
    detail: str = "Could not parse the paylaod. Expected a JPEG image of size (224, 224)."
