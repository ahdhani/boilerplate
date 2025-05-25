from app.db.models.product import Product
from app.utils.base.repository import RepositoryBase


class ProductRepository(RepositoryBase[Product]):
    model = Product
