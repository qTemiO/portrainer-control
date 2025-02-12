from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings import settings
from api.routers import all_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="portrainer-control",
    description="",
    lifespan=lifespan
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

for router in all_routers:
    app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, reload=False)
