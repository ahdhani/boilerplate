from typing import Any, Dict, List, Optional, Sequence

from fastapi import Depends
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from app.db.session import get_session


class QueryUtil:
    """Utility class for executing common database query operations."""

    def __init__(self, db: AsyncSession = Depends(get_session)):
        """Initialize QueryUtil with a database session.

        Args:
            db: AsyncSession instance for database operations
        """
        self.db = db

    async def query_all(self, statement: Select) -> Sequence[Any]:
        """Execute a query and return all results as scalars.

        Args:
            statement: SQLAlchemy select statement

        Returns:
            Sequence of scalar results
        """
        res: Result = await self.db.execute(statement=statement)
        return res.scalars()

    async def query_one(self, statement: Select) -> Optional[Any]:
        """Execute a query and return a single scalar result.

        Args:
            statement: SQLAlchemy select statement

        Returns:
            Single scalar result or None if no results
        """
        res: Result = await self.db.execute(statement=statement)
        return res.scalar()

    async def query_rows(self, statement: Select) -> list[Any]:
        """Execute a query and return all rows.

        Args:
            statement: SQLAlchemy select statement

        Returns:
            List of row results
        """
        res: Result = await self.db.execute(statement=statement)
        return res.all()

    async def query_rows_as_dicts(self, statement: Select) -> list[dict[str, Any]]:
        """Execute a query and return all rows as dictionaries.

        Args:
            statement: SQLAlchemy select statement

        Returns:
            List of dictionaries representing rows
        """
        res: Result = await self.db.execute(statement=statement)
        return res.mappings().all()

    async def query_loaded_rows(self, statement: Select) -> Sequence[Any]:
        """Execute a query and return unique scalar results.

        Args:
            statement: SQLAlchemy select statement

        Returns:
            Sequence of unique scalar results
        """
        res: Result = await self.db.execute(statement=statement)
        return res.unique().scalars()

    async def query_row(self, statement: Select) -> Optional[Any]:
        """Execute a query and return the first row.

        Args:
            statement: SQLAlchemy select statement

        Returns:
            First row or None if no results
        """
        res: Result = await self.db.execute(statement=statement)
        return res.first()

    async def query_row_as_dict(self, statement: Select) -> Optional[dict[str, Any]]:
        """Execute a query and return the first row as a dictionary.

        Args:
            statement: SQLAlchemy select statement

        Returns:
            Dictionary representing first row or None if no results
        """
        res: Result = await self.db.execute(statement=statement)
        return res.mappings().first()

    async def query_single_column_list(self, statement: Select) -> list[Any]:
        """Execute a query and return all results as a list of scalar values.

        Args:
            statement: SQLAlchemy select statement

        Returns:
            List of scalar values
        """
        res: Result = await self.db.execute(statement=statement)
        return res.scalars().all()

    async def run_stmt(self, statement: Any) -> None:
        """Execute a statement and commit the transaction.

        Args:
            statement: SQLAlchemy statement to execute
        """
        await self.db.execute(statement)
        await self.db.commit()

    async def bulk_insert(self, objects: list) -> None:
        self.db.add_all(objects)
        return await self.db.commit()
