from sqlalchemy import select
from sqlalchemy.orm import Session
from starlite import Provide, ResponseSpec, get
from starlite.controller import Controller as Base
from starlite.status_codes import HTTP_404_NOT_FOUND

from gwserver import model
from gwserver.api.schema import CATEGORY, UID, error
from gwserver.api.schema.error import ApiException
from gwserver.core.database import DB


class Controller(Base):
    @get(dependencies={"db": Provide(DB)})
    async def list_category(self, db: Session) -> list[CATEGORY]:
        stmt = select(model.Category)
        return [CATEGORY(uid=i.uid, title=i.title) for i in db.scalars(stmt)]

    @get(
        path="{uid:int}",
        dependencies={"db": Provide(DB)},
        responses={
            HTTP_404_NOT_FOUND: ResponseSpec(
                model=error.NOT_FOUND,
                description="Category not found",
            )
        },
    )
    async def get_category(self, uid: UID, db: Session) -> CATEGORY:
        record = db.get(model.Category, uid)

        if record is None:
            raise ApiException(error.NOT_FOUND)

        return CATEGORY(uid=record.uid, title=record.title)
