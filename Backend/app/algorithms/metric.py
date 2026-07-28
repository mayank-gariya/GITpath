from pydantic import BaseModel

class SearchMetrics(BaseModel):
    api_calls: int
    cache_hits: int
    cache_misses: int
    search_time: float
    expanded_nodes: int
    max_queue_size: int
    average_branching_factor: float