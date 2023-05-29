from abc import ABC
from collections.abc import Sequence
from typing import Generic

from litestar import Router
from litestar.di import Provide

from gwserver.core.database import DB
from gwserver.interface import base as Interface
from gwserver.interface.base.typings import Mapper, ResponseList, ResponseOne

from . import handler


class Base(Router, ABC, Generic[Mapper, ResponseOne]):
    def __init__(
        self,
        interface: Interface.Base[Mapper, ResponseOne],
        path: str,
        tags: Sequence[str] | None = None,
    ) -> None:
        super().__init__(
            path,
            tags=tags,
            route_handlers=[handler.get_one(interface)],
            dependencies={"session": Provide(DB, sync_to_thread=True)},
        )


class Listable(Base[Mapper, ResponseOne], Generic[Mapper, ResponseOne, ResponseList]):
    def __init__(
        self,
        interface: Interface.Listable[Mapper, ResponseOne, ResponseList],
        path: str,
        tags: Sequence[str] | None = None,
    ) -> None:
        super().__init__(interface, path, tags)
        self.register(handler.list_all(interface))
