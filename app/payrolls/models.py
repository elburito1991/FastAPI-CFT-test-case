from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database import Base


class PayRolls(Base):
    __tablename__ = "payrolls"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    salary = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)


class NextPayRolls(Base):
    __tablename__ = "next_payrolls"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    salary = Column(Integer, nullable=False)
    next_date = Column(Date, nullable=False)
