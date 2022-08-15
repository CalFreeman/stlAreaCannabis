from app.db.repositories.base import BaseRepository
from app.models.companies import CompanyCreate, CompanyUpdate, CompanyInDB


CREATE_COMPANY_QUERY = """
    INSERT INTO companies (name)
    VALUES (:name)
    RETURNING id, name;
"""


class CompaniesRepository(BaseRepository):
    """"
    All database actions associated with the Companies resource
    """

    async def create_companies(self, *, new_company: CompanyCreate) -> CompanyInDB:
        query_values = new_company.dict()
        companies = await self.db.fetch_one(query=CREATE_COMPANY_QUERY, values=query_values)

        return CompanyInDB(**companies)

