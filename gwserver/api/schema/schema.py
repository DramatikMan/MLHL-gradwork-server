from typing import Optional

from pydantic import BaseModel, ConstrainedInt

from gwserver import typings


class UID(ConstrainedInt):
    ge = 1


class IMAGE(BaseModel):
    uid: UID
    path: str
    category: Optional[typings.CATEGORY]


class CATEGORY(BaseModel):
    uid: UID
    title: typings.CATEGORY
