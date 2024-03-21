from dataclasses import dataclass
from typing import Optional


@dataclass
class Response:
    status_code: int
    message: Optional[str] = None
