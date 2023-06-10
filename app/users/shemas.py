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


class SNewUser(BaseModel):
    id: int
    login: str
    first_name: str
    last_name: str
    middle_name: str


class SUserLogin(BaseModel):
    id: int
    login: str
    first_name: str
    last_name: str
    middle_name: str
    access_token: str


class SUserMe(BaseModel):
    id: int
    login: str
    first_name: str
    last_name: str
    middle_name: str
