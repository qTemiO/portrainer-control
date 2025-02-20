from pydantic import BaseModel


class Environment(BaseModel):
    id: int
    name: str
    url: str
    total_containers: int
    running_containers: int
    stopped_containers: int
    healthy_containers: int
    unhealthy_containers: int
    stack_count: int
    status: int


class Container(BaseModel):
    id: str
    state: str
    names: list[str]
    image: str
    ports: list[str]


class Registry(BaseModel):
    id: int
    name: str


class Image(BaseModel):
    name: str
