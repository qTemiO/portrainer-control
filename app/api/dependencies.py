from typing import Annotated

from fastapi import Depends

from modules.commander.service import AgentsCommander

commander = Annotated[Depends(AgentsCommander), "Portainer commander service"]
