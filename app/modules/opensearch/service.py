import zlib
import httpx
import requests
from fastapi import Request

from settings import settings


class OpenSearch():

    def __init__(self):
        pass

    async def send_proxy_request_dashboards(self, request: Request, path: str):
        async with httpx.AsyncClient(verify=False) as client:
            headers = {
                "Content-Type": request.headers.get("Content-Type", ""),
            }

            response = await client.request(
                method=request.method, headers=headers, url=f"{settings.opensearch_url}/{path}",
                auth=requests.auth.HTTPBasicAuth(
                    username=settings.OPENSEARCH_DASHBOARDS_RO_LOGIN,
                    password=settings.OPENSEARCH_DASHBOARDS_RO_PASSWORD
                ), params=request.query_params, content=await request.body()
            )

        return httpx.Response(
            status_code=response.status_code, content=response.content, headers=dict(response.headers)
        )
