import signal
from ..utils.singleton import SingletonMeta 
from ..utils.logger import log

class Signal(metaclass=SingletonMeta):
    
    stop_signal: bool = False
    
    def _stop_signal_handler(self, sig, frame):
        log().info("Stopping server now")
        self.stop_signal = True
    
    def capture(self):
        signal.signal(signal.SIGINT, self._stop_signal_handler)
        signal.signal(signal.SIGTERM, self._stop_signal_handler) 