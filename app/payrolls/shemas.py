from datetime import date

from pydantic import BaseModel


class SNewPayroll(BaseModel):
    id: int
    user_id: int
    salary: int
    start_date: date

