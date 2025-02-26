import requests
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse

from settings import settings

class OpenSearch():

    def __init__(self):
        pass

    def send_proxy_request_dashboards(self, request: Request, path: str):
        headers = {
            "Content-Type": request.headers.get("Content-Type", ""),
        }
        url = f"{settings.opensearch_url}/{path}"

        response = requests.request(auth = requests.auth.HTTPBasicAuth(
            username=settings.OPENSEARCH_DASHBOARDS_RO_LOGIN,
            password=settings.OPENSEARCH_DASHBOARDS_RO_PASSWORD
        ), method=request.method, headers=headers, url=url, params=request.query_params, timeout=60.0)

        # return response
        if response.status_code:
            return RedirectResponse(url=f"{settings.opensearch_url}/{path}", headers=response.headers)
        else:
            raise HTTPException(status_code=503, detail="Opensearch did not acked")