from pydantic import BaseModel

class Shadow(BaseModel):
    username: str
    old_password: str
    new_password: str
    