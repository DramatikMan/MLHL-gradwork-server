import sqlalchemy as sa
import starlite as s

from gwserver import model
from gwserver.api.schema import CATEGORY, UID
from gwserver.core.database import DB


class Controller(s.Controller):
    @s.get(dependencies={"db": s.Provide(DB)})
    async def list_category(self, db: sa.orm.Session) -> list[CATEGORY]:
        stmt = sa.select(model.Category)
        return [CATEGORY(uid=i.uid, title=i.title) for i in db.scalars(stmt)]

    @s.get(path="{uid:int}", dependencies={"db": s.Provide(DB)})
    async def get_category(self, uid: UID, db: sa.orm.Session) -> CATEGORY:
        record = db.get(model.Category, uid)

        if record is None:
            raise s.HTTPException(detail="Category not found by UID.", status_code=404)

        return CATEGORY(uid=record.uid, title=record.title)
