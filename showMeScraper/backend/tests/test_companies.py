import pytest
from typing import List, Union
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
        self, app: FastAPI, client: AsyncClient, test_company: CompanyInDB
    ) -> None:
        res = await client.get(
            app.url_path_for("companies:get-company-by-id", id=test_company.id)
        )
        assert res.status_code == HTTP_200_OK

        company = CompanyInDB(**res.json())
        assert company == test_company

    @pytest.mark.parametrize(
        "id, status_code", ((500, 404), (-1, 404), (None, 422),),
    )
    async def test_wrong_id_returns_error(self, app: FastAPI, client: AsyncClient, id: int, status_code: int) -> None:
        res = await client.get(app.url_path_for("companies:get-company-by-id", id=id))
        assert res.status_code == status_code

    async def test_get_all_companies_returns_valid_response(
        self, app: FastAPI, client: AsyncClient, test_company: CompanyInDB
    ) -> None:
        res = await client.get(app.url_path_for("companies:get-all-companies"))
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0        
        companies = [CompanyInDB(**l) for l in res.json()]
        assert test_company in companies

class TestUpdateCompany:
    @pytest.mark.parametrize(
        "attrs_to_change, values",
        (
            (["name"], ["new fake company name"]),
            (["name"], ["new fake company name2"]),
        ),
    )
    async def test_update_company_with_valid_input(
        self, 
        app: FastAPI, 
        client: AsyncClient, 
        test_company: CompanyInDB, 
        attrs_to_change: List[str], 
        values: List[str],
    ) -> None:
        company_update = {
            "company_update": {
                attrs_to_change[i]: values[i] for i in range(len(attrs_to_change))
            }
        }
        res = await client.put(
            app.url_path_for(
                "companies:update-company-by-id",
                id=test_company.id,
            ),
            json=company_update
        )
        assert res.status_code == HTTP_200_OK
        updated_company = CompanyInDB(**res.json())
        assert updated_company.id == test_company.id  # make sure it's the same company
        # make sure that any attribute we updated has changed to the correct value
        for i in range(len(attrs_to_change)):
            attr_to_change = getattr(updated_company, attrs_to_change[i])
            assert attr_to_change != getattr(test_company, attrs_to_change[i])
            assert attr_to_change == values[i] 
        # make sure that no other attributes' values have changed
        for attr, value in updated_company.dict().items():
            if attr not in attrs_to_change:
                assert getattr(test_company, attr) == value
    @pytest.mark.parametrize(
        "id, payload, status_code",
        (
            (-1, {"name": "test"}, 422),
            (0, {"name": "test2"}, 422),
            (500, {"name": "test3"}, 404),
            (1, None, 422),
        ),
    )
    async def test_update_company_with_invalid_input_throws_error(
        self,
        app: FastAPI,
        client: AsyncClient,
        id: int,
        payload: dict,
        status_code: int,
    ) -> None:
        company_update = {"company_update": payload}
        res = await client.put(
            app.url_path_for("companies:update-company-by-id", id=id),
            json=company_update
        )
        assert res.status_code == status_code