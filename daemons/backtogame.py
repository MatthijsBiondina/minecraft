from utils.logger import Logger
from daemons.daemon import Daemon
from dds.sharedarray import SharedArray
import numpy as np
from utils.exceptions import SkipTickException
import pyautogui

logger = Logger(__name__)


class BackToGameClickerDaemon(Daemon):
    def __init__(self):
        super().__init__(tick_rate=2)
        self.window_focus = SharedArray(
            topic="window_focus", shape=(1,), dtype=np.bool_
        )
        self.monitor = SharedArray(
            topic="monitor", shape=(1080, 1920, 3), dtype=np.uint8
        )
        self.game_active = SharedArray(topic="game_active", shape=(1,), dtype=np.bool_)

        self.back_to_game_template = np.load("res/templates/back_to_game_button.npy")
        self.disconnect_template = np.load("res/templates/disconnect_button.npy")

    def run(self):
        while True:
            try:

                if np.any(np.isnan(self.monitor.read())) or np.any(
                    np.isnan(self.monitor.read())
                ):
                    raise SkipTickException

                if self.window_focus.read(idx=0):
                    if self.on_main_menu():
                        self.click_back_to_game()
                        self.game_active.write(False, idx=0)
                    else:
                        self.game_active.write(True, idx=0)
                else:
                    self.game_active.write(False, idx=0)

            except SkipTickException:
                pass
            except Exception as e:
                logger.error(f"Error capturing screenshot: {e}")
            finally:
                self.sleep()

    def on_main_menu(self):
        back_to_game_img = self.monitor.read()[322:366, 823:1100, :]
        disconnect_img = self.monitor.read()[707:751, 823:1100, :]
        return np.allclose(
            back_to_game_img, self.back_to_game_template, atol=2
        ) or np.allclose(disconnect_img, self.disconnect_template, atol=2)

    def click_back_to_game(self):
        pyautogui.moveTo(x=960, y=345, duration=0.1)
        pyautogui.click(x=960, y=345)


if __name__ == "__main__":
    daemon = BackToGameClickerDaemon()
    daemon.run()
