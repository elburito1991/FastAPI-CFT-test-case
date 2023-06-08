from fastapi import APIRouter, Depends

from app.payrolls.dao import PayRollsDAO, NextPayRollsDAO
from app.users.dependencies import get_current_user
from app.users.exeptions import UserForbiddenException
from app.users.models import Users

router = APIRouter(
    prefix="/payrolls",
    tags=["Заработная плата"]
)


@router.get("/current_payroll", description='Текущая зарплата', status_code=200)
async def get_current_payroll(current_user: Users = Depends(get_current_user)):
    if current_user.su:
        raise UserForbiddenException

    payroll = await PayRollsDAO.get_actual_payroll(user_id=current_user.id)
    return f"Ваша текущая заработная плата состаляет - {payroll} руб."


@router.get("/next_payroll", description='Сумма и дата следующего повышения', status_code=200)
async def get_next_payroll(current_user: Users = Depends(get_current_user)):
    if current_user.su:
        raise UserForbiddenException

    next_payroll = await NextPayRollsDAO.find_one_or_none(user_id=current_user.id)
    return f"Будущие начисления заработной платы составят - {next_payroll.salary} руб." \
           f" начиная с даты - {next_payroll.next_date} "