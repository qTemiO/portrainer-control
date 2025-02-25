from modules.commander.router import router as commander_router
from modules.opensearch.router import router as opensearch_router

all_routers = [
    commander_router,
    opensearch_router,
]
