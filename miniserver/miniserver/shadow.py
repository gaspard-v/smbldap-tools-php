from typing import Optional
from .linux.tcp import ConsumerAbstract
from .linux.signal import Signal
from .models.shadow import Shadow
from .models.base import BaseRequest
from .models.enum.action import Action
from .linux.shadow import Chpasswd
from .exceptions.shadow import (
    UnknowUserException,
    WrongPasswordException,
    InvalidCredentialException,
    ImpossibleRollback,
)
from pydantic import ValidationError
import json


class ShadowConsumer(ConsumerAbstract):
    def __init__(self) -> None:
        self.signal = Signal()
        self.signal.capture()
        self.chpasswd: Optional[Chpasswd] = None

    def consume(self, data: bytearray) -> bytes:
        obj = json.loads(data)
        requests = BaseRequest(**obj)
        if Action.CHANGE_PASSWORD == requests.action:
            return self._change_password(requests)
        if Action.ROLLBACK == requests.action:
            return self._rollback()

        # Would never be reached
        return bytes()

    def _rollback(self) -> bytes:
        if not self.chpasswd:
            raise ImpossibleRollback()
        self.chpasswd.rollback()
        return self._get_response_message("Rollback is successfull", 200)

    def _change_password(self, requests: BaseRequest) -> bytes:
        shadow = Shadow(**requests.data)
        self.chpasswd = Chpasswd(
            shadow.username, shadow.old_password, shadow.new_password
        )
        self.chpasswd.verify_password().modify_password()
        return self._get_response_message("Password modified successfully", 200)

    def stop_loop(self):
        return self.signal.stop_signal

    def _handle_credential_exception(self) -> bytes:
        new_exception = InvalidCredentialException()
        return self._get_error_message(new_exception, 400)

    def client_disconnected_event(self, addr):
        if not self.chpasswd:
            return
        self.chpasswd.reset()

    def handle_error(self, error: Exception):
        credential_exception = (UnknowUserException, WrongPasswordException)
        user_exception = (
            ValidationError,
            json.decoder.JSONDecodeError,
            ImpossibleRollback,
        )
        if isinstance(error, credential_exception):
            return self._handle_credential_exception()
        if isinstance(error, user_exception):
            return self._get_error_message(error, 400)
        return super().handle_error(error)
