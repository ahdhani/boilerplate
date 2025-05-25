from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.product.schema import ProductInSchema
from app.core.product.service import ProductService
from app.db.models.product import Product


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def product_service(mock_repository):
    return ProductService(repository=mock_repository)


@pytest.mark.asyncio
async def test_create_product_success(product_service, mock_repository):
    # Arrange
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 1000,
        "stock": 10,
    }
    payload = ProductInSchema(**product_data)

    mock_product = MagicMock(spec=Product)
    mock_repository.save_object.return_value = mock_product

    # Act
    result = await product_service.create(payload)

    # Assert
    assert result == mock_product
    mock_repository.save_object.assert_called_once()
    saved_product = mock_repository.save_object.call_args[0][0]
    assert isinstance(saved_product, Product)
    assert saved_product.name == product_data["name"]
    assert saved_product.description == product_data["description"]
    assert saved_product.price == product_data["price"]
    assert saved_product.stock == product_data["stock"]


@pytest.mark.asyncio
async def test_create_product_with_negative_price_raises_validation_error(
    product_service,
):
    # Arrange
    with pytest.raises(ValueError):
        ProductInSchema(
            name="Test Product", description="Test Description", price=-100, stock=10
        )


@pytest.mark.asyncio
async def test_create_product_with_negative_stock_raises_validation_error(
    product_service,
):
    # Arrange
    with pytest.raises(ValueError):
        ProductInSchema(
            name="Test Product", description="Test Description", price=1000, stock=-1
        )
