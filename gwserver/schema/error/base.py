from abc import ABC, abstractmethod
from typing import Any, Type

from pydantic import BaseModel, create_model
from starlite import HTTPException


class Base(ABC, HTTPException):
    def __init__(
        self,
        name: str,
        status_code: int,
        description: str,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(detail=description, status_code=status_code, headers=headers)
        self._name = name
        self._description = description

        self.response: dict[int | str, dict[str, Any]] = {
            self.status_code: {
                "model": self._get_model(),
                "description": description,
            }
        }

    @abstractmethod
    def _get_model(self) -> Type[BaseModel]:
        ...


class StaticAPIError(Base):
    def _get_model(self) -> Type[BaseModel]:
        return create_model(self._name, detail=self._description)


class DynamicAPIError(Base):
    def _get_model(self) -> Type[BaseModel]:
        return create_model(self._name, detail=(str, ...))

    def __call__(self, detail: str) -> HTTPException:
        return HTTPException(self.status_code, detail, headers=self.headers)
