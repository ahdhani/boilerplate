from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Any, Generic, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi import Depends, Path, params
from fastapi.routing import APIRouter
from pydantic import create_model
from starlette import status

from app.utils.base.schema import (
    PaginatedResponseSchema,
    SchemaBase,
)
from app.utils.base.service import ServiceBase

# Define type variables for generic types
ServiceType = TypeVar("ServiceType", bound=ServiceBase)
SchemaInType = TypeVar("SchemaInType", bound=SchemaBase)
SchemaOutType = TypeVar("SchemaOutType", bound=SchemaBase)


class CoreRouter(
    APIRouter,
    Generic[SchemaInType, SchemaOutType, ServiceType],
    metaclass=ABCMeta,
):
    """
    Base router class that provides common CRUD endpoints.
    Generic parameters:
    - SchemaInType: Pydantic model for create/update operations
    - SchemaOutType: Pydantic model for response data
    - ServiceType: The service class that handles business logic
    """

    id_type: Type[int | str | UUID] = int

    def __init__(
        self,
        tags: Optional[list[Union[str, Enum]]] = None,
        dependencies: list[params.Depends] | None = None,
        **kwargs,
    ):
        if dependencies is None:
            dependencies = []

        super().__init__(
            dependencies=dependencies,
            tags=tags,
            **kwargs,
        )

    @property
    @abstractmethod
    def service(self) -> Type[ServiceType]:
        """Return the service class for this router."""
        pass

    @property
    @abstractmethod
    def schema_out(self) -> Type[SchemaOutType]:
        """Return the output schema for this router."""
        pass

    def add_all_endpoints(self, in_schema):
        """Set up the CRUD routes for this router."""
        self.add_get_endpoint()
        self.add_create_endpoint(in_schema)
        self.add_delete_endpoint()
        self.add_list_endpoint()

        return self

    def add_get_endpoint(
        self,
        path: str = "/{id}",
        response_model: Type[SchemaOutType] | None = None,
        **kwargs,
    ):
        """Add GET endpoint to retrieve a single item by ID."""

        @self.get(
            path,
            response_model=response_model or self.schema_out,
            status_code=status.HTTP_200_OK,
            **kwargs,
        )
        async def get_item(
            id: self.id_type,
            service: ServiceType = Depends(self.service),
        ) -> SchemaOutType:
            return await service.get(id)

        return self

    def add_create_endpoint(
        self,
        in_schema: Type[SchemaInType],
        path: str = "/",
        response_model: Type[SchemaOutType] | None = None,
        status_code: int = status.HTTP_201_CREATED,
        **kwargs,
    ):
        """Add POST endpoint to create a new item."""

        @self.post(
            path,
            response_model=response_model or self.schema_out,
            status_code=status_code,
            **kwargs,
        )
        async def create_item(
            payload: in_schema,
            service: ServiceType = Depends(self.service),
        ) -> SchemaOutType:
            return await service.create(payload)

        return self

    def add_delete_endpoint(
        self,
        path: str = "/{id}",
        **kwargs,
    ):
        """Add DELETE endpoint to remove an item."""

        @self.delete(path, status_code=status.HTTP_204_NO_CONTENT, **kwargs)
        async def delete_item(
            id: self.id_type,
            service: ServiceType = Depends(self.service),
        ) -> None:
            await service.delete(id)

    def add_list_endpoint(
        self,
        response_model: Type[PaginatedResponseSchema] | None = None,
        **kwargs,
    ):
        """Add GET endpoint to list items with pagination."""
        response_model = response_model or self._get_paginated_response_model()

        @self.get("/", response_model=response_model, **kwargs)
        async def list_items(
            page: int = 1,
            page_size: int = 10,
            service: ServiceType = Depends(self.service),
        ) -> dict[str, Any]:
            return await service.list_paginated(
                page_number=page - 1, page_size=page_size
            )

    def _get_paginated_response_model(self) -> Type[PaginatedResponseSchema]:
        """Create a paginated response model for list endpoints."""
        name = f"Paginated{self.schema_out.__name__}"
        return create_model(
            name,
            records=(list[self.schema_out], []),  # type: ignore
            __base__=PaginatedResponseSchema,
        )
