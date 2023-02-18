from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlite import HTTPException, Provide, ResponseSpec
from starlite.controller import Controller as Base
from starlite.handlers import get
from starlite.status_codes import HTTP_404_NOT_FOUND

from gwserver import model, typings
from gwserver.api.schema import UID, error
from gwserver.core.database import DB


class IMAGE(BaseModel):
    uid: UID
    path: str
    category: typings.CATEGORY


class Controller(Base):
    @get(
        path="{uid:int}",
        dependencies={"db": Provide(DB)},
        responses={
            HTTP_404_NOT_FOUND: ResponseSpec(
                model=error.NOT_FOUND,
                description="Image not found",
            )
        },
    )
    async def get_image(self, uid: UID, db: Session) -> IMAGE:
        record = db.get(model.Image, uid)

        if record is None:
            raise HTTPException(**error.NOT_FOUND().dict())

        return IMAGE(
            uid=record.uid,
            path=record.path,
            category=record.category.title,
        )
