from abc import ABC, abstractmethod
from typing import Type

from litestar.exceptions import HTTPException
from litestar.openapi.datastructures import ResponseSpec
from pydantic import BaseModel, create_model


class Base(ABC, HTTPException):
    def __init__(
        self,
        name: str,
        status_code: int,
        description: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=description, headers=headers)
        self._name = name
        self._description = description

        self.response: dict[int, ResponseSpec] = {
            self.status_code: ResponseSpec(
                data_container=self._get_model(),
                description=description,
                generate_examples=False,
            )
        }

    @abstractmethod
    def _get_model(self) -> Type[BaseModel]:
        ...


class StaticAPIError(Base):
    def _get_model(self) -> Type[BaseModel]:
        return create_model(self._name, detail=(str, self._description))


class DynamicAPIError(Base):
    def _get_model(self) -> Type[BaseModel]:
        return create_model(self._name, detail=(str, ...))

    def __call__(self, detail: str) -> HTTPException:
        return HTTPException(
            status_code=self.status_code,
            detail=detail,
            headers=self.headers,
        )
