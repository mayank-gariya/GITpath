from fullapp.app.github.client import GitHubClient

class GitHubService:

    def __init__(self):
        self.client = GitHubClient()

    def get_user(self, username):
        return self.client.get_user(username)

    def get_followers(self, username):
        return self.client.get_followers(username)

    def get_following(self, username):
        return self.client.get_following(username)
