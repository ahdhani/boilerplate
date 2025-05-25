from pydantic import Field

from app.utils.base.schema import SchemaBase


class ProductInSchema(SchemaBase):
    name: str = Field(max_length=128)
    description: str = Field(max_length=1024)
    price: int = Field(ge=0)
    stock: int = Field(ge=0)


class ProductOutSchema(ProductInSchema):
    id: int = Field(serialization_alias="product_id")
