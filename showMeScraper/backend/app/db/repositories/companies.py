from app.db.repositories.base import BaseRepository
from app.models.companies import CompanyCreate, CompanyUpdate, CompanyInDB


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