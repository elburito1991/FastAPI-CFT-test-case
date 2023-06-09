from sqlalchemy import insert, select, update

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
        return result.scalar()

    @classmethod
    async def update_payroll(cls, user_id: int, **data):
        async with async_session_maker() as session:
            payroll_query = (
                update(cls.model).
                where(cls.model.user_id == user_id).
                values(**data).returning(cls.model)
            )
            result = await session.execute(payroll_query)
            await session.commit()
        return result.scalar()
