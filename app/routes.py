from fastapi import APIRouter

from app.core.product.api import router as product_router

root_router = APIRouter()
root_router.include_router(product_router, prefix="/product")
