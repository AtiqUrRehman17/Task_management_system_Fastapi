from pydantic import BaseModel
from typing import Optional, Generic, TypeVar
from datetime import datetime

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None