from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.models.companies import CompanyCreate, CompanyPublic, CompanyUpdate
from app.db.repositories.companies import CompaniesRepository  
from app.api.dependencies.database import get_repository  

router = APIRouter()

@router.get("/", response_model=List[CompanyPublic], name="companies:get-all-companies")
async def get_all_companies(
    companies_repo: CompaniesRepository = Depends(get_repository(CompaniesRepository)) 
) -> List[CompanyPublic]:
    return await companies_repo.get_all_companies() 

@router.post("/", response_model=CompanyPublic, name="companies:create-company", status_code=HTTP_201_CREATED)
async def create_new_company(
    new_company: CompanyCreate = Body(..., embed=True),
    companies_repo: CompaniesRepository = Depends(get_repository(CompaniesRepository)),
) -> CompanyPublic:
    created_company = await companies_repo.create_company(new_company=new_company)

    return created_company

@router.get("/{id}/", response_model=CompanyPublic, name="companies:get-company-by-id")
async def get_company_by_id(
  id: int, companies_repo: CompaniesRepository = Depends(get_repository(CompaniesRepository))
) -> CompanyPublic:
    company = await companies_repo.get_company_by_id(id=id)
    if not company:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No company found with that id.")
    return company

@router.put(
    "/{id}/", 
    response_model=CompanyPublic, 
    name="companies:update-company-by-id",
)
async def update_company_by_id(
    id: int = Path(..., ge=1, title="The ID of the Company to update."),
    company_update: CompanyUpdate = Body(..., embed=True),
    companies_repo: CompaniesRepository = Depends(get_repository(CompaniesRepository)),
) -> CompanyPublic:
    updated_company = await companies_repo.update_company(
        id=id, company_update=company_update,
    )
    if not updated_company:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, 
            detail="No companies found with that id.",
        )
    return updated_company

@router.delete("/{id}/", response_model=int, name="companies:delete-company-by-id")
async def delete_company_by_id(
    id: int = Path(..., ge=1, title="The ID of the company to delete."),
    companies_repo: CompaniesRepository = Depends(get_repository(CompaniesRepository)),
) -> int:
    deleted_id = await companies_repo.delete_company_by_id(id=id)

    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, 
            detail="No company found with that id.",
        )

    return deleted_id