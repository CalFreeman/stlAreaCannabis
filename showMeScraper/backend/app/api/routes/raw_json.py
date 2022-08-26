from typing import List, Dict
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from fastapi.encoders import jsonable_encoder
from app.models.raw_json import RawJsonCreate, RawJsonPublic, RawJsonUpdate
from app.db.repositories.raw_json import RawJsonRepository  
from app.api.dependencies.database import get_repository  

router = APIRouter()

@router.get("/", response_model=List[RawJsonPublic], name="raw_json:get-all-raw-json")
async def get_all_raw_json(
    raw_json_repo: RawJsonRepository = Depends(get_repository(RawJsonRepository)) 
) -> List[RawJsonPublic]:
    return await raw_json_repo.get_all_raw_json() 

@router.post("/", response_model=RawJsonPublic, name="raw_json:create-raw-json", status_code=HTTP_201_CREATED)
async def create_new_raw_json(
    new_raw_json: RawJsonCreate = Body(..., embed=True),
    raw_json_repo: RawJsonRepository = Depends(get_repository(RawJsonRepository)),
) -> RawJsonPublic:
    created_raw_json = await raw_json_repo.create_raw_json(new_raw_json=new_raw_json)
    return created_raw_json

@router.get("/{id}/", response_model=RawJsonPublic, name="raw_json:get-raw-json-by-id")
async def get_raw_json_by_id(
  id: int, raw_json_repo: RawJsonRepository = Depends(get_repository(RawJsonRepository))
) -> RawJsonPublic:
    raw_json = await raw_json_repo.get_raw_json_by_id(id=id)
    if not raw_json:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No raw_json found with that id.")
    return raw_json

@router.put(
    "/{id}/", 
    response_model=RawJsonPublic, 
    name="raw_json:update-raw-json-by-id",
)
async def update_raw_json_by_id(
    id: int = Path(..., ge=1, title="The ID of the raw_json to update."),
    raw_json_update: RawJsonUpdate = Body(..., embed=True),
    raw_json_repo: RawJsonRepository = Depends(get_repository(RawJsonRepository)),
) -> RawJsonPublic:
    updated_raw_json = await raw_json_repo.update_raw_json(
        id=id, raw_json_update=raw_json_update,
    )
    if not updated_raw_json:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, 
            detail="No raw_json found with that id.",
        )
    return updated_raw_json

@router.delete("/{id}/", response_model=int, name="raw_json:delete-raw-json-by-id")
async def delete_raw_json_by_id(
    id: int = Path(..., ge=1, title="The ID of the raw_json to delete."),
    raw_json_repo: RawJsonRepository = Depends(get_repository(RawJsonRepository)),
) -> int:
    deleted_id = await raw_json_repo.delete_raw_json_by_id(id=id)

    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, 
            detail="No raw_json found with that id.",
        )

    return deleted_id