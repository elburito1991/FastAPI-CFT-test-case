from fastapi import FastAPI

from app.admin.router import router as router_admin
from app.payrolls.router import router as router_payrolls
from app.users.router import router as router_auth

app = FastAPI()

app.include_router(router=router_auth)
app.include_router(router=router_payrolls)
app.include_router(router=router_admin)
