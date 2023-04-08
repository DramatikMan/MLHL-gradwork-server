from typing import Type

from sqlalchemy.sql.elements import ColumnElement

from gwserver.model import Category as Mapper
from gwserver.schema.response import Category as Response
from gwserver.schema.response import Category as ResponseList

from .base import Listable


class Interface(Listable[Mapper, Response, Response]):
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
                "title": rec.title,
            }
        )

    @classmethod
    def _where_uid(cls, uid: int) -> ColumnElement[bool]:
        return Mapper.uid == uid

    # * Listable
    @property
    def _response_schema_list(self) -> Type[Response]:
        return Response

    @classmethod
    def _to_json_list(cls, rec: Mapper) -> ResponseList:
        return cls._to_json(rec)


interface = Interface()
