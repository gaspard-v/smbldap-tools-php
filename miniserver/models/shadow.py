from pydantic import BaseModel

class Shadow:
    username: str
    old_password: str
    new_password: str
    