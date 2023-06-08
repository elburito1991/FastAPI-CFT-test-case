async def test_get_current_payroll(authenticated_admin_ac, authenticated_user_ac):
    await authenticated_admin_ac.post("/admin/set_payroll", params={
        "user_id": 3,
        "salary": 10000
    })
    response = await authenticated_user_ac.get("/payrolls/current_payroll")
    assert response.status_code == 200


async def test_get_next_payroll(authenticated_admin_ac, authenticated_user_ac):
    await authenticated_admin_ac.post("/admin/set_payroll", params={
        "user_id": 3,
        "salary": 10000
    })
    response = await authenticated_user_ac.get("/payrolls/next_payroll")
    assert response.status_code == 200
