from fastapi import APIRouter
from app.api.routes.companies import router as companies_router

router = APIRouter()

router.include_router(companies_router, prefix="/companies", tags=["companies"])