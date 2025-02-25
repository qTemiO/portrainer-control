from pydantic import BaseModel


class Logopass(BaseModel):
    login: str
    password: str
