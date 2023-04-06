import sqlalchemy as sa
import starlite as s

from gwserver.core.database import DB
from gwserver.model import Category as Mapper
from gwserver.schema.request import UID
from gwserver.schema.response import CATEGORY


class View(s.Controller):
    @s.get(dependencies={"db": s.Provide(DB)})
    async def list_category(self, db: sa.orm.Session) -> list[CATEGORY]:
        stmt = sa.select(Mapper)
        return [CATEGORY.parse_obj({"uid": i.uid, "title": i.title}) for i in db.scalars(stmt)]

    @s.get(path="{uid:int}", dependencies={"db": s.Provide(DB)})
    async def get_category(self, uid: UID, db: sa.orm.Session) -> CATEGORY:
        record: Mapper | None = db.get(Mapper, uid)

        if record is None:
            raise s.HTTPException(detail="Category not found by UID.", status_code=404)

        return CATEGORY.parse_obj({"uid": record.uid, "title": record.title})
