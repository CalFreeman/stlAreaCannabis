from typing import List

from fastapi import APIRouter, Body, Depends  
from starlette.status import HTTP_201_CREATED  

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

