from pydantic import BaseModel
from typing import List, Optional
from graph.node import GraphNode

class Edge(BaseModel):
    source: str
    target: str

class SearchGraph(BaseModel):
    nodes: List[GraphNode] = []
    edges: List[Edge] = []

class SearchResult(BaseModel):
    found: bool
    path: List[str]
    visited_count: int
    search_depth: int
    api_calls: int
    elapsed_time: float
    graph: SearchGraph 

class ProgressUpdate(BaseModel):
    type: str = "progress" 
    visited_count: int
    current_node: str
    graph: SearchGraph
    result: Optional[SearchResult] = None