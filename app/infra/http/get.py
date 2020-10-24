from typing import Any, Dict, Optional, Tuple

import requests
from requests.packages.urllib3.util.retry import Retry

from app.infra.http.timeout import TimeoutHTTPAdapter

retries = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "POST", "OPTIONS"],
)


def get(
    *, url: str, params: Optional[Dict[str, str]] = None, timeout: int = 40
) -> Tuple[bool, Dict[str, Any]]:
    if params:
        parameters = [key + "=" + str(parameter) for key, parameter in params.items()]
        parameters = "&".join(parameters)
        url += "?" + parameters

    try:
        with requests.Session() as client:
            client.mount(
                "https://", TimeoutHTTPAdapter(timeout=timeout, max_retries=retries),
            )
            client.mount(
                "http://", TimeoutHTTPAdapter(timeout=timeout, max_retries=retries),
            )
            response = client.get(url)
            response = response.json() if response.status_code == 200 else None
            return True, response
    except Exception as e:
        print(e)
        return False, None
