import asyncio

import pytest
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import get_session
from app.main import app
from tests.integration.utils.session import engine, get_test_session


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create tables once for the entire test session and drop them afterward."""

    async def async_setup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def async_cleanup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    # Run setup
    asyncio.run(async_setup())
    yield
    # Run cleanup
    asyncio.run(async_cleanup())


@pytest.fixture(scope="function")
def fix_client(setup_database):
    """Override the get_session dependency and provide a shared test client."""

    async def override_get_session():
        async with get_test_session() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client
