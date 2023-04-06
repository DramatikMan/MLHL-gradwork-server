from typing import Optional

from color_utils.typings import COLOR_RGB, COLOR_RYB
from pydantic import BaseModel

from gwserver import typings as t


class CATEGORY(BaseModel):
    uid: int
    title: t.CATEGORY


class IMAGE(BaseModel):
    uid: int
    path: str
    category: Optional[CATEGORY]
    color_RGB: Optional[COLOR_RGB]
    color_RYB: Optional[COLOR_RYB]
