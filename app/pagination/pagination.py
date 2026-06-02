from pydantic import BaseModel
from typing import Optional


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 10
    sort_by: Optional[str] = None
    sort_order: str = "asc"