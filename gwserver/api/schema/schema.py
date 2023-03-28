from typing import Optional

from pydantic import BaseModel, ConstrainedInt

from gwserver import typings as t


class UID(ConstrainedInt):
    ge = 1


class IMAGE(BaseModel):
    uid: UID
    path: str
    category: Optional[t.CATEGORY]
    color_RGB: Optional[t.COLOR_RGB]
    color_RYB: Optional[t.COLOR_RYB]


class CATEGORY(BaseModel):
    uid: UID
    title: t.CATEGORY
