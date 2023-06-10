from datetime import timedelta

from sqlalchemy import select, update

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.payrolls.exeptions import PayRollIsNotPresentException
from app.payrolls.models import NextPayRolls, PayRolls


class PayRollsDAO(BaseDAO):
    model = PayRolls

    @classmethod
    async def get_actual_payroll(cls, user_id: int):
        async with async_session_maker() as session:
            start_date_query = (
                select(PayRolls.start_date)
                .select_from(PayRolls)
                .where(PayRolls.user_id == user_id)
            )

            next_date_query = (
                select(NextPayRolls.next_date)
                .select_from(NextPayRolls)
                .where(NextPayRolls.user_id == user_id)
            )
            start_date = (await session.execute(start_date_query)).scalar()
            next_date = (await session.execute(next_date_query)).scalar()

            if not (start_date and next_date):
                raise PayRollIsNotPresentException

            if start_date >= next_date:
                next_payroll_query = (
                    select(NextPayRolls.next_date, NextPayRolls.salary)
                    .select_from(NextPayRolls)
                    .where(NextPayRolls.user_id == user_id)
                )

                next_payroll = (await session.execute(next_payroll_query)).mappings().all()
                new_date, new_salary = next_payroll[0]['next_date'], next_payroll[0]['salary']

                current_payroll_query = (
                    update(PayRolls).
                    where(PayRolls.user_id == user_id).
                    values(salary=new_salary,
                           start_date=new_date)
                )
                await session.execute(current_payroll_query)

                changed_next_payrolls = (
                    update(NextPayRolls).
                    where(NextPayRolls.user_id == user_id).
                    values(salary=int(new_salary * 1.3),
                           next_date=new_date + timedelta(days=90))
                )
                await session.execute(changed_next_payrolls)
                await session.commit()

            payroll_query = (
                select(PayRolls.__table__.columns)
                .select_from(PayRolls)
                .where(PayRolls.user_id == user_id)
            )

            result = await session.execute(payroll_query)
            return result.mappings().one_or_none()


class NextPayRollsDAO(BaseDAO):
    model = NextPayRolls
