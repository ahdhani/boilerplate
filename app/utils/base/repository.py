from abc import abstractmethod
from collections.abc import Sequence
from math import ceil
from typing import Any, Generic, TypeVar, Union, cast
from uuid import UUID

from fastapi import Depends
from sqlalchemy import Select, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import LoaderOption

from app.db.base import IdMixinBase
from app.db.session import get_session
from app.utils.base.query_util import QueryUtil
from app.utils.fastapi_utils.exception import ConflictException, NotFoundException

ModelType = TypeVar("ModelType", bound=IdMixinBase)
id_type = Union[UUID | int | str]


class RepositoryBase(QueryUtil, Generic[ModelType]):
    """Base repository class with common database operations.

    Provides CRUD operations and pagination support for SQLAlchemy models.
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_session),
    ) -> None:
        """Initialize the repository with a database session.

        Args:
            db: AsyncSession for database operations. Injected by FastAPI's dependency system.
        """
        super().__init__(db=db)

    @property
    @abstractmethod
    def model(self) -> type[ModelType]:
        """Return the SQLAlchemy model class associated with this repository."""
        ...

    async def get_one(self, model_id: id_type) -> ModelType | None:
        """Get a single record by ID.

        Args:
            model_id: The ID of the record to retrieve.

        Returns:
            The model instance if found, None otherwise.
        """
        stmt = select(self.model).where(self.model.id == model_id)
        return await self.query_one(stmt)

    async def get(self, model_id: id_type) -> ModelType:
        """Get a single record by ID or raise an exception if not found.

        Args:
            model_id: The ID of the record to retrieve.

        Returns:
            The model instance.

        Raises:
            NotFoundException: If no record is found with the given ID.
        """
        if obj := await self.get_one(model_id):
            return obj
        raise NotFoundException(f"{self.model.__name__} with id {model_id} not found")

    async def save_object(
        self, obj: ModelType, *, refresh: bool = True, **refresh_attrs: Any
    ) -> ModelType:
        """Save an object to the database.

        Args:
            obj: The model instance to save.
            refresh: Whether to refresh the object from the database.
            **refresh_attrs: Additional attributes to refresh.

        Returns:
            The saved model instance.

        Raises:
            ConflictException: If a unique constraint is violated.
        """
        self.db.add(obj)
        try:
            await self.db.commit()
            if refresh:
                await self.db.refresh(obj, **refresh_attrs)
            return obj
        except IntegrityError as e:
            await self.db.rollback()
            if (
                "UNIQUE constraint failed" in str(e)
                or "duplicate key" in str(e).lower()
            ):
                raise ConflictException(
                    "A record with these details already exists."
                ) from e
            raise  # Re-raise other IntegrityError cases

    async def list(
        self,
        page_number: int = 0,
        page_size: int = 100,
        options: Sequence[LoaderOption] | None = None,
    ) -> Sequence[ModelType]:
        """List records with pagination.

        Args:
            page_number: The page number (0-based).
            page_size: The number of items per page.
            options: Optional SQLAlchemy loader options.

        Returns:
            A sequence of model instances.
        """
        stmt = select(self.model)
        if options:
            stmt = stmt.options(*options)
        stmt = stmt.limit(page_size).offset(page_number * page_size)
        return await self.query_all(stmt)

    async def delete(self, model_id: id_type) -> None:
        """Delete a record by ID.

        Args:
            model_id: The ID of the record to delete.

        Raises:
            NotFoundException: If no record is found with the given ID.
        """
        obj = await self.get(model_id)
        await self.db.delete(obj)
        await self.db.commit()

    async def get_rowcount(self, stmt: Select[tuple[Any]]) -> int:
        """Get the total count of records matching a query.

        Args:
            stmt: The SQLAlchemy select statement to count results for.

        Returns:
            The count of matching records.
        """
        count_stmt = select(func.count()).select_from(stmt.subquery())
        result = await self.query_one(count_stmt)
        return cast(int, result)

    async def list_paginated(
        self,
        page_number: int = 0,
        page_size: int = 100,
        options: Sequence[LoaderOption] | None = None,
    ) -> dict[str, Any]:
        """List records with pagination metadata.

        Args:
            page_number: The page number (0-based).
            page_size: The number of items per page.
            options: Optional SQLAlchemy loader options.

        Returns:
            A dictionary containing:
                - records: The paginated results
                - record_count: Total number of records
                - page_count: Total number of pages
        """
        stmt = select(self.model)
        if options:
            stmt = stmt.options(*options)

        limit_stmt = stmt.limit(page_size).offset(page_number * page_size)
        records = await self.query_all(limit_stmt)

        row_count = await self.get_rowcount(stmt)
        page_count = ceil(row_count / page_size) if page_size > 0 else 0

        return {
            "records": records,
            "record_count": row_count,
            "page_count": page_count,
        }


RepositoryType = TypeVar("RepositoryType", bound=RepositoryBase)
