from typing import Optional

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
    color_RGB: Optional[t.COLOR_RGB]
    color_RYB: Optional[t.COLOR_RYB]
