from sqlalchemy import delete

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.payrolls.dao import NextPayRollsDAO, PayRollsDAO
from app.payrolls.models import NextPayRolls, PayRolls
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def delete_user(cls, user_id: int):
        async with async_session_maker() as session:

            get_payroll = await PayRollsDAO.find_one_or_none(user_id=user_id)
            get_next_payroll = await NextPayRollsDAO.find_one_or_none(user_id=user_id)

            if get_payroll:
                del_payroll = delete(PayRolls).where(
                    PayRolls.user_id == user_id
                )
                await session.execute(del_payroll)

            if get_next_payroll:
                del_next_payroll = delete(NextPayRolls).where(
                    NextPayRolls.user_id == user_id
                )
                await session.execute(del_next_payroll)

            del_user = delete(Users).where(
                Users.id == user_id
            )
            await session.execute(del_user)

            await session.commit()
