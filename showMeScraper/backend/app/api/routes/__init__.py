from fastapi import APIRouter
from app.api.routes.companies import router as companies_router
from app.api.routes.dispensaries import router as dispensaries_router  


router = APIRouter()

router.include_router(companies_router, prefix="/companies", tags=["companies"])
router.include_router(dispensaries_router, prefix="/dispensaries", tags=["dispensaries"])