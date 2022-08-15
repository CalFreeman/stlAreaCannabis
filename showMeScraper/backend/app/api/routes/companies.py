from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.models.companies import CompanyCreate, CompanyPublic  
from app.db.repositories.companies import CompaniesRepository  
from app.api.dependencies.database import get_repository  

router = APIRouter()

@router.get("/")
async def get_all_companies() -> List[dict]:
    companies = [
        {"id": 1, "name": "My house"},
        {"id": 2, "name": "Someone else's house"}
    ]

    return companies

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