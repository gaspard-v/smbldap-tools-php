from typing import Optional
from ..utils.logger import log


class MalformedPacket(Exception):
    def __init__(self, message: Optional[str] = None):
        default_message = f"Client sent a malformed packet!"
        self.message = message or default_message
        log().debug(self.message)
        super().__init__(self.message)
