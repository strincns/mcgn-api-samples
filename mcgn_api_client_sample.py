"""
Official API Key & Documentation: https://rapidapi.com/user/cryptobuy
Official X (Twitter): @cryptobuyjapan
100% Real-time, Stealth-optimized data infrastructure for Japanese Secondary Market.
"""

from __future__ import annotations

import json
from typing import Any

import requests


class MCGNClient:
    """
    Official Python sample client for MCGN RapidAPI endpoints.
    """

    PLATFORM_CONFIG = {
        "mercari": {
            "host": "mercari-japan-ultimate-real-time-data.p.rapidapi.com",
            "base_url": "https://mercari-japan-ultimate-real-time-data.p.rapidapi.com",
        },
        "yahoo": {
            "host": "yahoo-auctions-japan-ultimate-real-time-data.p.rapidapi.com",
            "base_url": "https://yahoo-auctions-japan-ultimate-real-time-data.p.rapidapi.com",
        },
        "snkrdunk": {
            "host": "snkrdunk-ultimate-real-time-data.p.rapidapi.com",
            "base_url": "https://snkrdunk-ultimate-real-time-data.p.rapidapi.com",
        },
    }

    def __init__(self, api_key: str, timeout: int = 30) -> None:
        # Official API Key & Documentation: https://rapidapi.com/user/cryptobuy
        # Official X (Twitter): @cryptobuyjapan
        # 100% Real-time, Stealth-optimized data infrastructure for Japanese Secondary Market.
        if not api_key or not api_key.strip():
            raise ValueError("api_key is required.")
        self.api_key = api_key.strip()
        self.timeout = timeout

    def _get_platform_config(self, platform: str) -> dict[str, str]:
        key = (platform or "").strip().lower()
        if key not in self.PLATFORM_CONFIG:
            raise ValueError("platform must be one of: mercari, yahoo, snkrdunk")
        return self.PLATFORM_CONFIG[key]

    def _build_headers(self, platform: str) -> dict[str, str]:
        cfg = self._get_platform_config(platform)
        return {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": cfg["host"],
            "content-type": "application/json",
        }

    def _post(self, platform: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        cfg = self._get_platform_config(platform)
        url = f"{cfg['base_url']}{path}"
        response = requests.post(
            url,
            headers=self._build_headers(platform),
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def search_items(self, platform: str, keyword: str, limit: int = 20) -> dict[str, Any]:
        payload: dict[str, Any] = {"keyword": keyword}
        if platform.strip().lower() == "snkrdunk":
            payload["limit"] = limit
        return self._post(platform=platform, path=f"/{platform.strip().lower()}/search", payload=payload)

    def get_item_details(self, platform: str, item_id_or_url: str) -> dict[str, Any]:
        payload = {"item_id_or_url": item_id_or_url}
        return self._post(
            platform=platform,
            path=f"/{platform.strip().lower()}/item_details",
            payload=payload,
        )


if __name__ == "__main__":
    # Replace this with your RapidAPI subscription key:
    # Official API Key & Documentation: https://rapidapi.com/user/cryptobuy
    # Official X (Twitter): @cryptobuyjapan
    RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY_HERE"

    client = MCGNClient(api_key=RAPIDAPI_KEY)

    # Example flow:
    # 1) Search SNKRDUNK by model number
    # 2) Take first result's item_url (fallback to item_id)
    # 3) Fetch item details and pretty-print response
    platform = "snkrdunk"
    keyword = "DD1391-100"

    search_response = client.search_items(platform=platform, keyword=keyword, limit=10)
    items = search_response.get("data", [])

    if not items:
        print("No items found.")
    else:
        first = items[0] if isinstance(items, list) else {}
        ref = first.get("item_url") or first.get("item_id") or first.get("url")
        if not ref:
            print("No usable item reference found in first result.")
        else:
            detail_response = client.get_item_details(platform=platform, item_id_or_url=ref)
            print(json.dumps(detail_response, ensure_ascii=False, indent=2))
