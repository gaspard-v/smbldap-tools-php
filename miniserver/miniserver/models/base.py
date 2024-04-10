from pydantic import BaseModel
from .enum.action import Action


class BaseRequest(BaseModel):
    action: Action
    data: dict
