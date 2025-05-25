from sqlalchemy import CheckConstraint, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import AuditMixin, Base, IdIntMixin


class Product(IdIntMixin, AuditMixin, Base):
    __tablename__ = "product"
    name: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(1024))
    price: Mapped[float] = mapped_column(
        Float, CheckConstraint("price >= 0", name="non_negative_price"), nullable=False
    )
    stock: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("stock >= 0", name="non_negative_stock"),
        nullable=False,
        default=0,
    )
