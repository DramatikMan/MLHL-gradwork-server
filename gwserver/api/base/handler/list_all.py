import sqlalchemy as sa
from litestar import get
from litestar.handlers import HTTPRouteHandler

from gwserver.interface import base as Interface
from gwserver.interface.base.typings import Mapper, ResponseList, ResponseOne


def list_all(interface: Interface.Listable[Mapper, ResponseOne, ResponseList]) -> HTTPRouteHandler:
    async def handler(session: sa.orm.Session) -> list[ResponseList]:
        return interface.ls(session)

    handler.__annotations__["return"] = list[
        interface._response_schema_list  # type: ignore[name-defined]
    ]

    return get()(handler)
