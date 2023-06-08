from fastapi import HTTPException, status


class PayRollException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class PayRollIsNotPresentException(PayRollException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Запись по заработной плате отсуствует, обратитесь к администратору"
