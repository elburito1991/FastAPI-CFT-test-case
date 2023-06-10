from fastapi import APIRouter, Depends

from app.payrolls.dao import NextPayRollsDAO, PayRollsDAO
from app.payrolls.exeptions import PayRollIsNotPresentException
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
    return payroll


@router.get("/next_payroll", description='Сумма и дата следующего повышения', status_code=200)
async def get_next_payroll(current_user: Users = Depends(get_current_user)):
    if current_user.su:
        raise UserForbiddenException

    next_payroll = await NextPayRollsDAO.find_one_or_none(user_id=current_user.id)
    if not next_payroll:
        raise PayRollIsNotPresentException
    return next_payroll
