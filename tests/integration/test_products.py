from fastapi import status


class TestProductAPI:
    base_url = "api/v1/product"

    def test_create_product_success(self, fix_client, product_data):
        response = fix_client.post(f"{self.base_url}/", json=product_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "product_id" in data
        assert data["name"] == product_data["name"]
        assert data["description"] == product_data["description"]
        assert data["price"] == product_data["price"]
        assert data["stock"] == product_data["stock"]

    def test_create_duplicate_product_fails(self, fix_client, product_data):
        # Arrange - Create first product
        response = fix_client.post(f"{self.base_url}/", json=product_data)
        assert response.status_code == status.HTTP_201_CREATED

        # Act - Try to create duplicate
        response = fix_client.post(f"{self.base_url}/", json=product_data)

        # Assert
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_get_product_success(self, fix_client, product_data):
        # Arrange - Create a product
        create_response = fix_client.post(f"{self.base_url}/", json=product_data)
        product_id = create_response.json()["product_id"]

        # Act
        response = fix_client.get(f"{self.base_url}/{product_id}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["product_id"] == product_id
        assert data["name"] == product_data["name"]

    def test_get_nonexistent_product_returns_404(self, fix_client):
        # Act
        response = fix_client.get(f"{self.base_url}/999999")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_products(self, fix_client, product_data):
        # Arrange - Create multiple products
        for i in range(3):
            product_data["name"] = f"Product {i}"
            fix_client.post(f"{self.base_url}/", json=product_data)

        # Act
        response = fix_client.get(f"{self.base_url}/?page=1&page_size=2")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "records" in data
        assert "record_count" in data
        assert "page_count" in data
        assert len(data["records"]) == 2
        assert data["record_count"] >= 3

    def test_create_product_validation_error(self, fix_client):
        # Arrange - Invalid product data (negative price and stock)
        invalid_data = {
            "name": "Invalid Product",
            "description": "This should fail validation",
            "price": -100,
            "stock": -1,
        }

        # Act
        response = fix_client.post(f"{self.base_url}/", json=invalid_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        errors = response.json()["detail"]
        assert any(
            ["Input should be greater than or equal to 0" in str(err) for err in errors]
        )
