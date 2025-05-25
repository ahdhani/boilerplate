from fastapi import HTTPException


class ExceptionBase(HTTPException):
    pass


class SystemException(HTTPException):
    def __init__(self, error):
        super().__init__(status_code=500, detail=error)


class NotFoundException(ExceptionBase):
    def __init__(self, detail):
        super().__init__(status_code=404, detail=detail)


class BadRequestException(ExceptionBase):
    def __init__(self, detail):
        super().__init__(status_code=400, detail=detail)


class UnauthorizedException(ExceptionBase):
    def __init__(self, detail):
        super().__init__(status_code=401, detail=detail)


class UnprocessableEntity(ExceptionBase):
    def __init__(self, detail):
        super().__init__(status_code=422, detail=detail)


class ConflictException(ExceptionBase):
    def __init__(self, detail: str):
        super().__init__(status_code=409, detail=detail)
