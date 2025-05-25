import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def product_data():
    return {
        "name": "Test Product",
        "description": "A test product description",
        "price": 1000,  # $10.00
        "stock": 10,
    }
