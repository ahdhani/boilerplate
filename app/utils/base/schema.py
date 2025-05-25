from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class SchemaBase(BaseModel): ...


class PaginationSchema(SchemaBase):
    page_size: int = Field(10, gt=0, le=100)
    page_number: int = Field(1, gt=0)

    @field_validator("page_number")
    @classmethod
    def decrement_page_number(cls, page_number):
        return page_number - 1


class PaginatedResponseSchema(SchemaBase):
    records: list
    page_count: int
    record_count: int


class DateTimeRangeOptional(SchemaBase):
    start_time: datetime | None = None
    end_time: datetime | None = None
