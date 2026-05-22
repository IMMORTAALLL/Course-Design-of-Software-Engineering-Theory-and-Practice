from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


class ParamValidationError(AppException):
    def __init__(self, message: str = "参数校验失败"):
        super().__init__(40001, message)


class ResourceNotFoundError(AppException):
    def __init__(self, message: str = "资源不存在"):
        super().__init__(40002, message)


class StateNotAllowedError(AppException):
    def __init__(self, message: str = "状态不允许"):
        super().__init__(40003, message)


class UnauthorizedError(AppException):
    def __init__(self, message: str = "未登录"):
        super().__init__(40101, message)


class TokenInvalidError(AppException):
    def __init__(self, message: str = "Token无效或已过期"):
        super().__init__(40102, message)


class ForbiddenError(AppException):
    def __init__(self, message: str = "权限不足"):
        super().__init__(40301, message)


class ConflictError(AppException):
    def __init__(self, message: str = "资源冲突"):
        super().__init__(40901, message)


class InternalError(AppException):
    def __init__(self, message: str = "系统内部错误"):
        super().__init__(50001, message)
