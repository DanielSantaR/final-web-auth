import logging
from typing import Any, Dict, Optional

from httpx import AsyncClient, Auth
from pydantic import AnyHttpUrl

log = logging.getLogger(__name__)


class HTTPXClient:
    async def get(
        self,
        *,
        url_service: AnyHttpUrl,
        status_response: int,
        timeout: float = 20,
        auth: Optional[Auth] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:

        try:
            async with AsyncClient() as client:
                response = await client.get(
                    url_service,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    timeout=timeout,
                    auth=auth,
                )
                json_response = (
                    response.json() if response.status_code == status_response else None
                )
                return json_response
        except Exception as e:
            log.error(e)
            return None

    async def post(
        self,
        *,
        url_service: AnyHttpUrl,
        status_response: int,
        timeout: float = 20,
        auth: Optional[Auth] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, Any]] = None,
        xml: Optional[bool] = False
    ) -> Optional[Dict[str, Any]]:

        try:
            async with AsyncClient() as client:
                response = await client.post(
                    url_service,
                    params=params,
                    json=body,
                    data=data,
                    headers=headers,
                    cookies=cookies,
                    timeout=timeout,
                    auth=auth,
                )
                if response.status_code == status_response:
                    if xml:
                        response = response.text
                    else:
                        response = response.json()
                else:
                    response = None
                return response
        except Exception as e:
            log.error(e)
            return None

    async def put(
        self,
        *,
        url_service: AnyHttpUrl,
        status_response: int,
        timeout: float = 20,
        auth: Optional[Auth] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:

        try:
            async with AsyncClient() as client:
                response = await client.put(
                    url_service,
                    params=params,
                    json=body,
                    data=data,
                    headers=headers,
                    cookies=cookies,
                    timeout=timeout,
                    auth=auth,
                )

                json_response = (
                    response.json() if response.status_code == status_response else None
                )
                return json_response
        except Exception as e:
            log.error(e)
            return None

    async def delete(
        self,
        *,
        url_service: AnyHttpUrl,
        status_response: int,
        timeout: float = 20,
        auth: Optional[Auth] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:

        try:
            async with AsyncClient() as client:
                response = await client.delete(
                    url_service,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    timeout=timeout,
                    auth=auth,
                )
                json_response = 1 if response.status_code == status_response else None
                return json_response
        except Exception as e:
            log.error(e)
            return None

    async def patch(
        self,
        *,
        url_service: AnyHttpUrl,
        body: bytes,
        status_response: int,
        auth: Optional[Auth] = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> bool:
        try:
            async with AsyncClient() as client:
                response = await client.patch(
                    url_service, data=body, headers=headers, auth=auth
                )

                response = True if response.status_code == status_response else False
                return response
        except Exception as e:
            log.error(e)
            return False
