from typing import Annotated

from fastapi import Depends

from modules.commander.service import AgentsCommander
from utils import get_commander

# commander = Annotated[AgentsCommander, Depends(get_commander)]
