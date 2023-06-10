import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("login, password, first_name, last_name, middle_name, status_code", [
    (
        "some_login",
        "some_password",
        "some_first_name",
        "some_last_name",
        "some_middle_name",
        200
    ),
    (
        "some_login",
        "some_pasword",
        "some_frst_name",
        "some_lst_name",
        "some_mddle_name",
        409
    ),

])
async def test_register_user(login, password, first_name, last_name, middle_name, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "login": login,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("login, password, status_code", [
    (
        "admin",
        "admin",
        200
    )
])
async def test_login_user(login, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "login": login,
        "password": password,
    })

    assert response.status_code == status_code
