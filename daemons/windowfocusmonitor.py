import numpy as np
from daemons.daemon import Daemon
from dds.sharedarray import SharedArray
from utils.tools import get_active_window_title
from utils.logger import Logger

logger = Logger(__name__)


class WindowFocusMonitorDaemon(Daemon):
    def __init__(self):
        super().__init__(tick_rate=10)
        self.array = SharedArray(topic="window_focus", shape=(1,), dtype=np.bool_)

    def run(self):
        while True:
            try:
                window_title = get_active_window_title().decode()
                is_focused = "Multiplayer (3rd-party Server)" in window_title
                self.array.write(is_focused, idx=0)
            except Exception as e:
                logger.error(f"Error writing to window focus array: {e}")
            finally:
                self.sleep()


if __name__ == "__main__":
    daemon = WindowFocusMonitorDaemon()
    daemon.run()
