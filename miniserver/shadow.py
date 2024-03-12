from .linux.tcp import ConsumerAbstract
from .linux.signal import Signal
from .models.shadow import Shadow
from .linux.shadow import Chpasswd
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

    def stop_loop(self):
        return self.signal.stop_signal