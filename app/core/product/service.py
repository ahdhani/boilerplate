from fastapi import Depends

from app.core.product.repository import ProductRepository
from app.core.product.schema import ProductInSchema
from app.db.models.product import Product
from app.utils.base.service import ServiceBase


class ProductService(ServiceBase[ProductRepository, Product, ProductInSchema]):
    def __init__(self, repository: ProductRepository = Depends(ProductRepository)):
        self.repository: ProductRepository = repository

    async def create(self, payload: ProductInSchema, **kwargs) -> Product:
        return await self.repository.save_object(
            Product(
                name=payload.name,
                price=payload.price,
                stock=payload.stock,
                description=payload.description,
            )
        )
