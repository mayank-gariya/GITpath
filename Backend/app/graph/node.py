from pydantic import BaseModel

class GraphNode(BaseModel):
    username: str
    avatar_url: str
    html_url: str