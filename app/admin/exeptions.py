from fastapi import HTTPException, status


class AdminException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class PayrollAlreadyExistsException(AdminException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Запись payrolls уже существует"


class PayrollNotExistsException(AdminException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Запись payrolls не существует"
