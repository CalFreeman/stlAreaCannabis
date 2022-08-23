from typing import List
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.repositories.base import BaseRepository
from app.models.companies import CompanyCreate, CompanyUpdate, CompanyInDB

# UPDATE_Company_BY_ID_QUERY = """
#     UPDATE cleanings  
#     SET name         = :name,  
#         description  = :description,  
#         price        = :price,  
#         cleaning_type = :cleaning_type  wwwwwwwwwwwww
#     WHERE id = :id  
#     RETURNING id, name, description, price, cleaning_type;  
# """

CREATE_COMPANY_QUERY = """
    INSERT INTO companies (name)
    VALUES (:name)
    RETURNING id, name;
"""
GET_COMPANY_BY_ID_QUERY = """
    SELECT id, name
    FROM companies
    WHERE id = :id;
"""

GET_ALL_COMPANIES_QUERY = """
    SELECT id, name 
    FROM companies;  
"""

UPDATE_COMPANY_BY_ID_QUERY = """
    UPDATE companies
    SET name = :name
    WHERE id = :id  
    RETURNING id, name; 
"""

DELETE_COMPANY_BY_ID_QUERY = """
    DELETE FROM companies  
    WHERE id = :id  
    RETURNING id;  
""" 

class CompaniesRepository(BaseRepository):
    """"
    All database actions associated with the Companies resource
    """

    async def create_company(self, *, new_company: CompanyCreate) -> CompanyInDB:
        query_values = new_company.dict()
        company = await self.db.fetch_one(query=CREATE_COMPANY_QUERY, values=query_values)

        return CompanyInDB(**company)

    async def get_company_by_id(self, *, id: int) -> CompanyInDB:
        company = await self.db.fetch_one(query=GET_COMPANY_BY_ID_QUERY, values={"id": id})
        if not company:
            return None
            
        return CompanyInDB(**company)
    async def get_all_companies(self) -> List[CompanyInDB]:
        companies_records = await self.db.fetch_all(
            query=GET_ALL_COMPANIES_QUERY,
        )
        return [CompanyInDB(**l) for l in companies_records]

    async def update_company(
        self, *, id: int, company_update: CompanyUpdate,
    ) -> CompanyInDB:
        company = await self.get_company_by_id(id=id)
        if not company:
            return None
        company_update_params = company.copy(
            update=company_update.dict(exclude_unset=True),
        )
        try:
            updated_company = await self.db.fetch_one(
                query=UPDATE_COMPANY_BY_ID_QUERY, 
                values=company_update_params.dict(),
            )
            return CompanyInDB(**updated_company)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, 
                detail="Invalid update params.",
            )

    async def delete_company_by_id(self, *, id: int) -> int:
        company = await self.get_company_by_id(id=id)
        if not company:
            return None
        deleted_id = await self.db.execute(
            query=DELETE_COMPANY_BY_ID_QUERY, 
            values={"id": id},
        )
        return deleted_id