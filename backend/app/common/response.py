from typing import Any, Optional

from pydantic import BaseModel


class ApiResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Optional[Any] = None


def success(data: Any = None, message: str = "success") -> dict:
    return {"code": 0, "message": message, "data": data}


def error(code: int, message: str) -> dict:
    return {"code": code, "message": message, "data": None}


def paginated(items: list, page: int, size: int, total: int) -> dict:
    return {
        "code": 0,
        "message": "success",
        "data": {
            "items": items,
            "page": page,
            "size": size,
            "total": total,
        },
    }
