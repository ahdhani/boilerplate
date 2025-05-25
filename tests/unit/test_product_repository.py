from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.product.repository import ProductRepository
from app.db.models.product import Product


@pytest.fixture
def repository():
    session = AsyncMock()
    return ProductRepository(db=session)


@pytest.mark.asyncio
async def test_save_product_success(repository):
    # Arrange
    product = Product(
        name="Test Product", description="Test Description", price=1000, stock=10
    )

    # Mock the save_object method
    repository.save_object = AsyncMock(return_value=product)

    # Act
    result = await repository.save_object(product)

    # Assert
    assert result == product
    repository.save_object.assert_awaited_once_with(product)


@pytest.mark.asyncio
async def test_get_product_by_id_success(repository):
    # Arrange
    product_id = 1
    expected_product = MagicMock(spec=Product)
    expected_product.id = product_id
    repository.get = AsyncMock(return_value=expected_product)

    # Act
    result = await repository.get(product_id)

    # Assert
    assert result == expected_product
    repository.get.assert_awaited_once_with(product_id)


@pytest.mark.asyncio
async def test_list_products_paginated(repository):
    # Arrange
    page_number = 0
    page_size = 10
    mock_products = [MagicMock(spec=Product) for _ in range(3)]

    # Mock the list_paginated method
    mock_result = {"records": mock_products, "record_count": 3, "page_count": 1}
    repository.list_paginated = AsyncMock(return_value=mock_result)

    # Act
    result = await repository.list_paginated(page_number, page_size)

    # Assert
    assert result == mock_result
    repository.list_paginated.assert_awaited_once_with(page_number, page_size)


@pytest.mark.asyncio
async def test_delete_product_success(repository):
    # Arrange
    product_id = 1
    mock_product = MagicMock(spec=Product)
    mock_product.id = product_id

    # Mock get method and db operations
    repository.get = AsyncMock(return_value=mock_product)
    repository.db = AsyncMock()

    # Act
    await repository.delete(product_id)

    # Assert
    repository.get.assert_awaited_once_with(product_id)
    repository.db.delete.assert_awaited_once_with(mock_product)
    repository.db.commit.assert_awaited_once()
