from typing import Optional

import color_utils.typings as color
from pydantic import BaseModel, ConstrainedInt

from gwserver import typings as t


class UID(ConstrainedInt):
    ge = 1


class CATEGORY(BaseModel):
    uid: int
    title: t.CATEGORY


class IMAGE(BaseModel):
    uid: int
    path: str
    category: Optional[CATEGORY]
    color_RGB: Optional[color.COLOR_RGB]
    color_RYB: Optional[color.COLOR_RYB]
