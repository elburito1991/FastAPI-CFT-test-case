from fastapi import APIRouter, Depends, Response

from app.users.exeptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.shemas import SUserAuth, SUserReg

router = APIRouter(
    prefix="/auth",
    tags=["Пользователи"]
)


@router.post("/register", status_code=200, description="Создать учетную запись")
async def register_user(user_data: SUserReg):
    existing_login = await UsersDAO.find_one_or_none(login=user_data.login)
    if existing_login:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    is_su = True if user_data.login == 'admin' else False

    await UsersDAO.add(
        login=user_data.login,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        middle_name=user_data.middle_name,
        su=is_su
    )


@router.post("/login", description="Зайти в учетную запись")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.login, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout", description="Выйти из учетной записи")
def logout_user(response: Response):
    response.delete_cookie("access_token")
    return "Success"


@router.get("/me", description="Текущие данные учетной записи")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user

