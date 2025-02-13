from pydantic import BaseModel


class Environment(BaseModel):
    id: int
    name: str


class Container(BaseModel):
    id: str
    state: str
    names: list[str]
    image: str
