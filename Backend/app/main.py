# app/main.py (or your test script)
from app.graph.builder import GraphBuilder
from app.graph.node import GraphNode

# 1. Define a mock service (or use your real one) that HAS the method
class MockGitHubService:
    def get_following(self, username: str):
        # returns a list of dicts with the expected keys
        if username == "octocat":
            return [
                {"login": "defunkt", "avatar_url": "...", "html_url": "..."},
                {"login": "pjhyett", "avatar_url": "...", "html_url": "..."},
            ]
        return []

# 2. Create an INSTANCE of the service
service = MockGitHubService() 

# 3. Pass the INSTANCE to the builder
builder = GraphBuilder(service) 

nodes = builder.get_neighbors("octocat")
print(nodes)