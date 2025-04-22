import time
import numpy as np
from mss import mss
from daemons.daemon import Daemon
from dds.sharedarray import SharedArray
from utils.logger import Logger
import cv2
from utils.exceptions import SkipTickException

logger = Logger(__name__)


class ScreencaptureDaemon(Daemon):
    """Daemon for capturing the screen and sending it to a DDS topic."""

    def __init__(self, monitor_index=1):
        super().__init__(tick_rate=5)
        self.sct = mss()
        self.monitor = self.sct.monitors[monitor_index]

        screen_width, screen_height = self.monitor["width"], self.monitor["height"]

        self.window_focus = SharedArray(
            topic="window_focus", shape=(1,), dtype=np.bool_
        )
        self.array = SharedArray(
            topic="monitor", shape=(screen_height, screen_width, 3), dtype=np.uint8
        )

    def run(self):
        while True:
            try:
                if not self.window_focus.read(idx=0):
                    raise SkipTickException
                screenshot = self.sct.grab(self.monitor)
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR)
                self.array.write(frame)
            except SkipTickException:
                pass
            except Exception as e:
                logger.error(f"Error capturing screenshot: {e}")
            finally:
                self.sleep()


if __name__ == "__main__":
    daemon = ScreencaptureDaemon()
    daemon.run()
