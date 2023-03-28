from typing import Optional

from pydantic import BaseModel, ConstrainedInt

from gwserver import typings as t


class UID(ConstrainedInt):
    ge = 1


class IMAGE(BaseModel):
    uid: UID
    path: str
    category: Optional[t.CATEGORY]


class CATEGORY(BaseModel):
    uid: UID
    title: t.CATEGORY
