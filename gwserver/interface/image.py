from typing import Type

from sqlalchemy.sql.elements import ColumnElement

from gwserver.model import Image as Mapper
from gwserver.schema.response import Image as Response

from .base import Base


class Interface(Base[Mapper, Response]):
    @property
    def _mapper(self) -> Type[Mapper]:
        return Mapper

    @property
    def _response_schema_one(self) -> Type[Response]:
        return Response

    @classmethod
    def _to_json(cls, rec: Mapper) -> Response:
        return Response.parse_obj(
            {
                "uid": rec.uid,
                "path": rec.path,
                "category": vars(rec.category) if rec.category is not None else None,
                "color_RGB": rec.color_rgb,
                "color_RYB": rec.color_ryb,
            }
        )

    @classmethod
    def _where_uid(cls, uid: int) -> ColumnElement[bool]:
        return Mapper.uid == uid


interface = Interface()
