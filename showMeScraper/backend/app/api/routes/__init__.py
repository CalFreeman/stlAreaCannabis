from fastapi import APIRouter
from app.api.routes.companies import router as companies_router
from app.api.routes.dispensaries import router as dispensaries_router  
from app.api.routes.raw_json import router as raw_json_router

router = APIRouter()

router.include_router(companies_router, prefix="/companies", tags=["companies"])
router.include_router(dispensaries_router, prefix="/dispensaries", tags=["dispensaries"])
router.include_router(raw_json_router, prefix="/raw_json", tags=["raw_json"])
