from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.admin.exeptions import PayrollAlreadyExistsException, PayrollNotExistsException
from app.payrolls.dao import PayRollsDAO, NextPayRollsDAO
from app.payrolls.shemas import SNewPayroll
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.exeptions import UserForbiddenException, UserNotExistsException
from app.users.models import Users

router = APIRouter(
    prefix="/admin",
    tags=["Инструменты модератора"]
)


@router.post("/set_payroll", response_model=SNewPayroll, description='Установка значения зарплаты', status_code=201)
async def set_current_payroll(user_id: int, salary: int, current_user: Users = Depends(get_current_user)):
    if not current_user.su or current_user.id == user_id:
        raise UserForbiddenException

    existing_user_login = await UsersDAO.find_one_or_none(id=user_id)
    if not existing_user_login:
        raise UserNotExistsException

    get_user_payroll = await PayRollsDAO.find_one_or_none(user_id=user_id)
    if get_user_payroll:
        raise PayrollAlreadyExistsException

    date_now = datetime.now(timezone.utc).date()

    new_payroll = await PayRollsDAO.add(
        user_id=user_id,
        salary=salary,
        start_date=date_now,
    )

    await NextPayRollsDAO.add(
        user_id=user_id,
        salary=int(salary * 1.3),
        next_date=date_now + timedelta(days=90)
    )

    return jsonable_encoder(new_payroll)


@router.put("/update_payroll", response_model=SNewPayroll, description='Обновление значения зарплаты', status_code=200)
async def update_current_payroll(user_id: int, salary: int, current_user: Users = Depends(get_current_user)):
    if not current_user.su:
        raise UserForbiddenException

    existing_user_login = await UsersDAO.find_one_or_none(id=user_id)
    if not existing_user_login:
        raise UserNotExistsException

    get_user_payroll = await PayRollsDAO.find_one_or_none(user_id=user_id)
    if not get_user_payroll:
        raise PayrollNotExistsException

    date_now = datetime.now(timezone.utc).date()

    updated_payroll = await PayRollsDAO.update_payroll(
        user_id,
        salary=salary,
        start_date=date_now,
    )

    await NextPayRollsDAO.update_payroll(
        user_id,
        salary=int(salary * 1.3),
        next_date=date_now + timedelta(days=90)
    )

    return jsonable_encoder(updated_payroll)


@router.delete("/delete/{user_id}", description='Удалить пользователя',  status_code=204)
async def del_user(user_id: int, current_user: Users = Depends(get_current_user)):
    if not current_user.su:
        raise UserForbiddenException

    user = await UsersDAO.find_one_or_none(id=user_id)
    if not user:
        raise UserNotExistsException

    await UsersDAO.delete_user(user_id)







