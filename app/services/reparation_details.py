from app.core.config import Settings, get_settings
from app.infra.httpx.client import HTTPXClient
from app.schemas.reparation_detail import (
    BaseReparationDetail,
    CreateReparationDetail,
    ReparationDetail,
    UpdateReparationDetail,
)

httpx_client = HTTPXClient()

settings: Settings = get_settings()


class ReparationDetailService:
    def __init__(self):
        return

    async def create_detail(
        self, *, employee_id: str, vehicle_id: str, detail: BaseReparationDetail
    ) -> ReparationDetail:
        url = f"{settings.DATABASE_URL}/api/details"
        header = {"Content-Type": "application/json"}
        body = CreateReparationDetail(
            **detail.dict(), employee_id=employee_id, vehicle_id=vehicle_id
        )
        response = await httpx_client.post(
            url_service=url,
            status_response=201,
            body=body.dict(),
            headers=header,
            timeout=40,
        )
        return response

    async def update_detail(
        self,
        *,
        employee_id: str,
        reparation_id: int,
        detail: UpdateReparationDetail,
    ) -> ReparationDetail:
        url = f"{settings.DATABASE_URL}/api/details/{reparation_id}"
        header = {"Content-Type": "application/json"}
        detail.employee_id = employee_id
        response = await httpx_client.patch(
            url_service=url,
            status_response=201,
            body=detail.dict(),
            headers=header,
            timeout=40,
        )
        return response

    async def get_by_vehicle(self, *, vehicle_id: str) -> ReparationDetail:
        url = f"{settings.DATABASE_URL}/api/details"
        header = {"Content-Type": "application/json"}
        response = await httpx_client.get(
            url_service=url,
            status_response=200,
            headers=header,
            params={"vehicle_id": vehicle_id},
            timeout=40,
        )
        return response

    async def get_by_owner(self, *, vehicle_id: str, owner_id: str) -> ReparationDetail:
        url = f"{settings.DATABASE_URL}/api/details"
        header = {"Content-Type": "application/json"}
        response = await httpx_client.get(
            url_service=url,
            status_response=200,
            headers=header,
            params={"vehicle_id": vehicle_id, "owner_id": owner_id},
            timeout=40,
        )
        return response

    async def get_by_id(self, *, reparation_id: int) -> ReparationDetail:
        url = f"{settings.DATABASE_URL}/api/details/{reparation_id}"
        header = {"Content-Type": "application/json"}
        response = await httpx_client.get(
            url_service=url, status_response=200, headers=header, timeout=40
        )
        return response

    async def delete_by_id(self, *, reparation_id: int) -> int:
        url = f"{settings.DATABASE_URL}/api/details/{reparation_id}"
        header = {"Content-Type": "application/json"}
        response = await httpx_client.delete(
            url_service=url, status_response=204, headers=header, timeout=40
        )
        return response


reparation_detail_service = ReparationDetailService()
