import time
from enum import Enum
from typing import List, Dict, Tuple
from app.graph.node import GraphNode
from app.github.service import GitHubService
from app.core.logger import get_logger
from app.core.constants import SearchDirection

logger = get_logger(__name__)

class GraphBuilder:
    def __init__(self, github_service: GitHubService, cache_ttl_seconds: int = 3600):
        # 1. Dependency Injection: Service is passed in rather than hardcoded
        self.github_service = github_service
        # Cache mapping: (username, direction) -> (timestamp, list of GraphNodes)
        self._cache: Dict[Tuple[str, SearchDirection], Tuple[float, List[GraphNode]]] = {}
        self.cache_ttl_seconds = cache_ttl_seconds
        self.api_calls = 0 

    def get_neighbors(self, username: str, direction: SearchDirection = SearchDirection.FOLLOWERS) -> List[GraphNode]:
        username_lower = username.lower().strip()
        cache_key = (username_lower, direction)
        current_time = time.time()

        # 2. Check the cache (and clean up if expired)
        if cache_key in self._cache:
            timestamp, cached_neighbors = self._cache[cache_key]
            if current_time - timestamp < self.cache_ttl_seconds:
                return cached_neighbors
            else:
                # 3. Memory Cleanup: Remove expired keys explicitly
                del self._cache[cache_key]

        # 4. Cache miss: Fetch from GitHub service using basic error handling
        self.api_calls += 1
        try:
            if direction == SearchDirection.FOLLOWERS:
                raw_neighbors = self.github_service.get_followers(username_lower)
            else:
                raw_neighbors = self.github_service.get_following(username_lower)
        except Exception as e:
            logger.exception(f"Failed to fetch neighbors for user {username_lower}: {e}")
            return []

        # 5. Parse into GraphNode objects
        neighbors = [
            GraphNode(
                username=user["login"],
                avatar_url=user["avatar_url"],
                html_url=user["html_url"],
            )
            for user in raw_neighbors
        ]

        # 6. Save to cache with the current timestamp
        self._cache[cache_key] = (current_time, neighbors)

        return neighbors