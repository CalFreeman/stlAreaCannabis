from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.models.dispensaries import DispensaryCreate, DispensaryUpdate, DispensaryPublic
from app.db.repositories.dispensaries import DispensariesRepository
from app.api.dependencies.database import get_repository  

router = APIRouter()

@router.get("/", response_model=List[DispensaryPublic], name="dispensary:get-all-dispensaries")
async def get_all_dispensaries(
    dispensary_repo: DispensariesRepository = Depends(get_repository(DispensariesRepository)) 
) -> List[DispensaryPublic]:
    return await dispensary_repo.get_all_dispensaries() 

@router.post("/", response_model=DispensaryPublic, name="dispensary:create-dispensary", status_code=HTTP_201_CREATED)
async def create_new_dispensary(
    new_dispensary: DispensaryCreate = Body(..., embed=True),
    dispensary_repo: DispensariesRepository = Depends(get_repository(DispensariesRepository)),
) -> DispensaryPublic:
    created_dispensary = await dispensary_repo.create_dispensary(new_dispensary=new_dispensary)

    return created_dispensary

@router.get("/{id}/", response_model=DispensaryPublic, name="dispensary:get-dispensary-by-id")
async def get_dispensary_by_id(
  id: int, dispensaries_repo: DispensariesRepository = Depends(get_repository(DispensariesRepository))
) -> DispensaryPublic:
    dispensary = await dispensaries_repo.get_dispensary_by_id(id=id)
    if not dispensary:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No dispensary found with that id.")
    return dispensary

@router.put(
    "/{id}/", 
    response_model=DispensaryPublic, 
    name="dispensary:update-dispensary-by-id",
)
async def update_dispensary_by_id(
    id: int = Path(..., ge=1, title="The ID of the dispensary to update."),
    dispensary_update: DispensaryUpdate = Body(..., embed=True),
    dispensary_repo: DispensariesRepository = Depends(get_repository(DispensariesRepository)),
) -> DispensaryPublic:
    updated_dispensary = await dispensary_repo.update_dispensary(
        id=id, dispensary_update=dispensary_update,
    )
    if not updated_dispensary:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, 
            detail="No dispensary found with that id.",
        )
    return updated_dispensary