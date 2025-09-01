import httpx
from typing import Any

DEFAULT_BASE = "https://jsonplaceholder.typicode.com"

class ExternalClient:
    def __init__(self, base_url: str = DEFAULT_BASE, timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def get(self, path: str, params: dict | None = None) -> Any:
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPStatusError as e:
            # Re-lanza como buena práctica; FastAPI lo atrapará si lo manejas a nivel de router
            raise
        except httpx.RequestError as e:
            # timeout, DNS, etc.
            raise
