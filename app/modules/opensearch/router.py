from fastapi import APIRouter, Request, Depends

from modules.opensearch.service import OpenSearch

router = APIRouter(prefix="/opensearch")

@router.api_route("/dashboards/{path:path}", methods=["GET", "POST"])
async def dashboards_proxy(request: Request, path: str, service: OpenSearch = Depends()):
    return await service.send_proxy_request_dashboards(request, path)
