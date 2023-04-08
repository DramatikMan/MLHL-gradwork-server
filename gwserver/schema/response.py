from color_utils.typings import COLOR_RGB, COLOR_RYB
from pydantic import BaseModel


class Category(BaseModel):
    uid: int
    title: str


class Image(BaseModel):
    uid: int
    path: str
    category: Category | None
    color_RGB: COLOR_RGB | None
    color_RYB: COLOR_RYB | None
