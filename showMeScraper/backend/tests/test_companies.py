import pytest

from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
)
from app.models.companies import CompanyCreate, CompanyInDB

# decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio  

@pytest.fixture
def new_company():
    return CompanyCreate(
        name="test company",
    )

class TestCompaniesRoutes:

    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("companies:create-company"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("companies:create-company"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestCreateCompany:
    async def test_valid_input_creates_company(
        self, app: FastAPI, client: AsyncClient, new_company: CompanyCreate
    ) -> None:
        res = await client.post(
            app.url_path_for("companies:create-company"), json={"new_company": new_company.dict()}
        )
        assert res.status_code == HTTP_201_CREATED
        
        created_company = CompanyCreate(**res.json())
        assert created_company == new_company
    @pytest.mark.parametrize(
        "invalid_payload, status_code",
        (
            (None, 422),
            ({}, 422),
        ),
    )
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient, invalid_payload: dict, status_code: int
    ) -> None:
        res = await client.post(
            app.url_path_for("companies:create-company"), json={"new_company": invalid_payload}
        )
        assert res.status_code == status_code

class TestGetCompany:
    async def test_get_company_by_id(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.get(
            app.url_path_for("companies:get-company-by-id", id=1)
        )
        assert res.status_code == HTTP_200_OK

        company = CompanyInDB(**res.json())
        assert company.id == 1