from dataclasses import asdict
from .linux.tcp import ConsumerAbstract
from .linux.signal import Signal
from .models.shadow import Shadow
from .linux.shadow import Chpasswd
from .exceptions.shadow import UnknowUserException, WrongPasswordException, InvalidCredentialException
from .models.tcp.error import build_error_response
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
    
    def handle_error(self, error: Exception):
        user_errors = (
            UnknowUserException, 
            WrongPasswordException
        )
        if not isinstance(error, user_errors):
            super().handle_error(error)
        
        new_exception = InvalidCredentialException()
        error_obj = build_error_response(
            400,
            str(type(new_exception)),
            new_exception.message
        )
        error_dict = asdict(error_obj)
        return json.dumps(error_dict).encode()
