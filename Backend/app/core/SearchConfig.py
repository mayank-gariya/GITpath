from pydantic import BaseModel, Field
from core.constants import SearchDirection

class SearchConfig(BaseModel):
    max_depth: int = Field(
        default=5,
        ge=1,
        le=10,
    )
    max_neighbors_per_user: int = Field(
        default=100,
        ge=1,
        le=500,
    )
    direction: SearchDirection = SearchDirection.FOLLOWERS