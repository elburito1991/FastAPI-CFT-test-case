from pydantic import BaseModel


class SUserReg(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str
    middle_name: str


class SUserAuth(BaseModel):
    login: str
    password: str
