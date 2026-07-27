from app.github.service import GitHubService

service = GitHubService()

profile = service.get_profile("octocat")

print(profile)