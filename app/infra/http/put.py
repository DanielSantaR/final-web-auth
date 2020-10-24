from typing import Any, Dict, Optional

import requests
from requests.packages.urllib3.util.retry import Retry

from app.infra.http.timeout import TimeoutHTTPAdapter

retries = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "POST", "OPTIONS"],
)


def put(*, url: str, json: Optional[Dict[str, Any]] = None, timeout: int = 40) -> bool:
    try:
        with requests.Session() as client:
            client.mount(
                "https://", TimeoutHTTPAdapter(timeout=timeout, max_retries=retries),
            )
            client.mount(
                "http://", TimeoutHTTPAdapter(timeout=timeout, max_retries=retries),
            )

            response = client.put(url, json=json)
            response = response.json() if response.status_code == 200 else None
            return response
    except Exception as e:
        print(e)
        return False
