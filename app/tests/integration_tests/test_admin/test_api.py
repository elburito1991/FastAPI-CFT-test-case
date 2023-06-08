from app.payrolls.dao import PayRollsDAO, NextPayRollsDAO
from app.users.dao import UsersDAO


async def test_admin_tools(authenticated_admin_ac, authenticated_user_ac):
    response = await authenticated_user_ac.post("/admin/set_payroll", params={
        "user_id": 2,
        "salary": 10000
    })
    assert response.status_code == 403

    await authenticated_admin_ac.post("/admin/set_payroll", params={
        "user_id": 2,
        "salary": 10000
    })
    new_payroll = await PayRollsDAO.find_one_or_none(user_id=2)
    new_next_payroll = await NextPayRollsDAO.find_one_or_none(user_id=2)
    assert new_payroll and new_next_payroll

    await authenticated_admin_ac.post("/admin/update_payroll", params={
        "user_id": 2,
        "salary": 15000
    })
    updated_payroll = await PayRollsDAO.find_one_or_none(user_id=2)
    updated_new_next_payroll = await NextPayRollsDAO.find_one_or_none(user_id=2)
    assert updated_payroll['salary'] == 15000 and updated_new_next_payroll['salary'] == int(15000 * 1.3)

    await authenticated_admin_ac.delete(f"/admin/delete/{2}")
    user = await UsersDAO.find_one_or_none(id=2)
    payroll = await PayRollsDAO.find_one_or_none(user_id=2)
    next_payroll = await NextPayRollsDAO.find_one_or_none(user_id=2)
    assert all(list(map(lambda el: el is None, [user, payroll, next_payroll])))
