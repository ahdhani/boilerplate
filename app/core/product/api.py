from app.core.product.schema import ProductInSchema, ProductOutSchema
from app.core.product.service import ProductService
from app.utils.base.router import CoreRouter


class ProductRouter(CoreRouter[ProductInSchema, ProductOutSchema, ProductService]):
    service = ProductService
    schema_out = ProductOutSchema


router = ProductRouter().add_all_endpoints(ProductInSchema)
