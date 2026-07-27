import unittest
from app.graph.builder import GraphBuilder
from app.graph.node import GraphNode

class MockGitHubService:
    def get_following(self, username: str):
        if username == "octocat":
            return [
                {
                    "login": "defunkt",
                    "avatar_url": "https://avatars.githubusercontent.com/u/2?v=4",
                    "html_url": "https://github.com/defunkt",
                },
                {
                    "login": "pjhyett",
                    "avatar_url": "https://avatars.githubusercontent.com/u/3?v=4",
                    "html_url": "https://github.com/pjhyett",
                },
            ]
        return []

class TestGraphBuilder(unittest.TestCase):
    def test_get_neighbors_octocat(self):
        service = MockGitHubService()
        builder = GraphBuilder(service)
        nodes = builder.get_neighbors("octocat")

        self.assertIsInstance(nodes, list)
        self.assertTrue(all(isinstance(n, GraphNode) for n in nodes))
        self.assertEqual(len(nodes), 2)       
        self.assertEqual(nodes[0].username, "defunkt")
        self.assertEqual(nodes[1].username, "pjhyett")

if __name__ == "__main__":
    unittest.main()