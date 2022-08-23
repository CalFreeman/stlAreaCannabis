from fastapi import APIRouter, Body, Depends, HTTPException, Path
from app.models.dispensaries import DispensaryUpdate, DispensaryPublic
from app.db.repositories.dispensaries import DispensaryRepository
from app.api.dependencies.database import get_repository  
from typing import List

router = APIRouter()

@router.get("/", response_model=List[DispensaryPublic], name="dispensary:get-all-dispensaries")
async def get_all_dispensaries(
    dispensary_repo: DispensaryRepository = Depends(get_repository(DispensaryRepository)) 
) -> List[DispensaryPublic]:
    return await dispensary_repo.get_all_dispensaries() 

@router.put(
    "/{id}/", 
    response_model=DispensaryPublic, 
    name="companies:update-dispensary-by-id",
)
async def update_DispensaryPublic_by_id(
    id: int = Path(..., ge=1, title="The ID of the dispensary to update."),
    dispensary_update: DispensaryUpdate = Body(..., embed=True),
    dispensary_repo: DispensaryRepository = Depends(get_repository(DispensaryRepository)),
) -> DispensaryPublic:
    updated_dispensary = await dispensary_repo.update_dispensary(
        id=id, dispensary_update=dispensary_update,
    )
    if not updated_dispensary:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, 
            detail="No dispensary found with that id.",
        )
    return updatdispensaryany