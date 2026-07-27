import httpx
from typing import Optional

from app.core.constants import GitHubAPI
from app.core.settings import settings
from app.core.logger import get_logger
from app.github.schemas import GitHubUser

logger = get_logger(__name__)

class GitHubClient:

    def __init__(self):
        self.client = httpx.Client(
            base_url=GitHubAPI.BASE_URL,
            timeout=settings.REQUEST_TIMEOUT,
            headers={
                **GitHubAPI.DEFAULT_HEADERS,
                "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
            },
        )

    def get_user(self, username: str) -> Optional[GitHubUser]:
        logger.info(f"Fetching profile: {username}")
        
        try:
            response = self.client.get(f"/users/{username}")

            if response.status_code == 200:
                logger.info("Profile fetched successfully.")
                return GitHubUser.model_validate(response.json())

            logger.error(
                f"GitHub request failed ({response.status_code}): {response.text}"
            )
            return None
            
        except httpx.RequestError as exc:
            logger.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            return None

    def close(self):
        """Close the underlying client connection pool."""
        self.client.close()