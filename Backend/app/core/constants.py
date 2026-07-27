"""
Application-wide constants.

Only values that are static and shared across the application
should live here.
"""

from enum import Enum


class GitHubAPI:
    BASE_URL = "https://api.github.com"
    API_VERSION = "2022-11-28"

    USERS = "/users"
    FOLLOWERS = "/followers"
    FOLLOWING = "/following"

    DEFAULT_HEADERS = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
    }


class Search:
    DEFAULT_MAX_DEPTH = 5
    DEFAULT_MAX_NEIGHBOURS = 100
    DEFAULT_TIMEOUT = 15


class Cache:
    DEFAULT_TTL = 300          
    MAX_CACHE_SIZE = 500


class LogMessages:
    APP_STARTED = "Application started."
    REQUEST_RECEIVED = "Request received."
    GITHUB_REQUEST = "Calling GitHub API."
    CACHE_HIT = "Cache hit."
    CACHE_MISS = "Cache miss."
    
class SearchDirection(Enum):
    FOLLOWERS = "followers"
    FOLLOWING = "following"