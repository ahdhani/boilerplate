from contextlib import asynccontextmanager
from typing import AsyncGenerator

import orjson
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db.session import orjson_serializer

db_name = "test.db"

# Create an asynchronous database engine
engine = create_async_engine(
    f"sqlite+aiosqlite:///./{db_name}",
    connect_args={"check_same_thread": False},
    json_serializer=orjson_serializer,
    json_deserializer=orjson.loads,
)
AsyncSessionFactory = async_sessionmaker(
    engine, autocommit=False, autoflush=False, expire_on_commit=False
)


@asynccontextmanager
async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session
