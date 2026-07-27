from typing import List
from app.graph.node import GraphNode

class GraphBuilder:
    def __init__(self, github_service):
        self.github_service = github_service  

    def get_neighbors(self, username: str) -> List[GraphNode]:
        following_data = self.github_service.get_following(username)
        return [
            GraphNode(
                username=user["login"],
                avatar_url=user["avatar_url"],
                html_url=user["html_url"],
            )
            for user in following_data
        ]