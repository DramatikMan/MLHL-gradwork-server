import sqlalchemy as sa
from litestar import get
from litestar.handlers import HTTPRouteHandler

from gwserver.interface import base as Interface
from gwserver.interface.base.typings import Mapper, ResponseOne
from gwserver.schema import error
from gwserver.schema.request import UID


def get_one(interface: Interface.Base[Mapper, ResponseOne]) -> HTTPRouteHandler:
    async def handler(uid: UID, session: sa.orm.Session) -> ResponseOne:
        return interface.get(uid, session)

    handler.__annotations__["return"] = interface._response_schema_one
    return get(path="{uid:int}", responses=error.NotFoundByUID.response)(handler)
