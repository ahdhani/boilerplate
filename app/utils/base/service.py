from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from fastapi import Depends

from app.utils.base.repository import ModelType, RepositoryType, id_type
from app.utils.base.schema import SchemaBase

SchemaInType = TypeVar("SchemaInType", bound=SchemaBase)


class ServiceBase(ABC, Generic[RepositoryType, ModelType, SchemaInType]):
    model: ModelType

    def __init__(self, repository: RepositoryType = Depends()):
        self.repository = repository

    @abstractmethod
    async def create(self, payload: SchemaInType, **kwargs) -> ModelType: ...

    async def get(self, model_id: id_type) -> ModelType:
        return await self.repository.get(model_id)

    async def delete(self, model_id: id_type):
        return await self.repository.delete(model_id)

    async def list_paginated(self, page_number, page_size) -> dict[str, Any]:
        return await self.repository.list_paginated(page_number, page_size)


ServiceType = TypeVar("ServiceType", bound=ServiceBase)
