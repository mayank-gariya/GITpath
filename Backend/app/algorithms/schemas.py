from pydantic import BaseModel

class SearchResult(BaseModel):
    found: bool
    path: list[str]
    visited_count: int
    search_depth: int
    elapsed_time: float

    api_calls: int