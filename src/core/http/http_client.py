import logging

logger = logging.getLogger(__name__)

import httpx
from typing import Any, Optional


class HttpClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        self._client = httpx.AsyncClient(base_url=self.base_url, headers=headers)

    async def get(self, endpoint: str, params: Optional[dict] = None) -> Any:
        try:
            response = await self._client.get(endpoint, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except httpx.HTTPStatusError as e:
            # Handle HTTP errors (e.g., 4xx, 5xx)
            logger.error(f"HTTP error occurred: {e}")
            return None
        except httpx.RequestError as e:
            # Handle network-related errors
            logger.error(f"An error occurred while requesting {e.request.url!r}: {e}")
            return None

    async def post(self, endpoint: str, data: dict) -> Any:
        try:
            response = await self._client.post(endpoint, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e}")
            return None
        except httpx.RequestError as e:
            logger.error(f"An error occurred while requesting {e.request.url!r}: {e}")
            return None

    async def close(self):
        await self._client.close()
