from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from typing_extensions import Annotated

cascade_default = "all, delete, delete-orphan"
datetime_default_now = Annotated[datetime, mapped_column(DateTime, default=func.now())]


int_pk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]


class Base(DeclarativeBase):
    @classmethod
    def columns(cls):
        return cls.__table__.columns


class BaseMixin:
    pass


class IdMixinBase(BaseMixin):
    id: Mapped


class IdIntMixin(IdMixinBase):
    id: Mapped[int_pk]


class AuditMixin(BaseMixin):
    created_at: Mapped[datetime_default_now]
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
