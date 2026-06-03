from pydantic import BaseModel
from typing import Optional


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 10
    sort_by: Optional[str] = None
    sort_order: str = "asc"

    @property
    def skip(self) -> int:
        """Calculate offset for SQL query based on current page."""
        return (self.page - 1) * self.page_size