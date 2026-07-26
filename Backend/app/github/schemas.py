from pydantic import BaseModel

class GitHubUser(BaseModel):
    id: int
    login: str
    name: str | None = None

    avatar_url: str
    html_url: str

    followers: int
    following: int

    public_repos: int

    bio: str | None = None