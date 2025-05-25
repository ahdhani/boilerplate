from typing import AsyncGenerator

import orjson
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import DBSettings


def orjson_serializer(obj):
    return orjson.dumps(
        obj, option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NAIVE_UTC, default=str
    ).decode()


db_settings = DBSettings()  # type: ignore
# Create an asynchronous database engine
engine = create_async_engine(
    str(db_settings.async_url),
    json_serializer=orjson_serializer,
    json_deserializer=orjson.loads,
    connect_args={},
)
AsyncSessionFactory = async_sessionmaker(
    engine, autocommit=False, autoflush=False, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session
