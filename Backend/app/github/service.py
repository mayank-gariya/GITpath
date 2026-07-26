from github.client import GitHubClient

class GitHubService:

    def __init__(self):

        self.client = GitHubClient()

    def get_profile(self, username: str):
        return self.client.get_user(username)