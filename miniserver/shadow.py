from dataclasses import asdict
from .linux.tcp import ConsumerAbstract
from .linux.signal import Signal
from .models.shadow import Shadow
from .linux.shadow import Chpasswd
from .exceptions.shadow import UnknowUserException, WrongPasswordException, InvalidCredentialException
from pydantic import ValidationError
import json

class ShadowConsumer(ConsumerAbstract):
    def __init__(self) -> None:
        self.signal = Signal()
        self.signal.capture()
    
    def consume(self, data: bytearray):
        obj = json.loads(data)
        shadow = Shadow(**obj)
        chpasswd = Chpasswd(shadow.username, shadow.old_password, shadow.new_password)
        chpasswd.verify_password()
        return "oof".encode()

    def stop_loop(self):
        return self.signal.stop_signal
    
    def _handle_credential_exception(self) -> bytes:
        new_exception = InvalidCredentialException()
        return self._get_error_message(
            new_exception,
            400
        )
    
    def handle_error(self, error: Exception):
        credential_exception = (
            UnknowUserException, 
            WrongPasswordException
        )
        user_exception = (
            ValidationError
        )
        if isinstance(error, credential_exception):
            return self._handle_credential_exception()
        if isinstance(error, user_exception):
            return self._get_error_message(error, 400)
        return super().handle_error(error)
        
