from collections import deque
import time
import numpy as np
import pyautogui
from daemons.daemon import Daemon
from dds.sharedarray import SharedArray
from game.player import Player
from utils.exceptions import SkipTickException
from utils.logger import Logger

logger = Logger(__name__)

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False


class MouseMovementController(Daemon):
    P = -20.0
    I = -0.0
    D = -0.1

    # Low-pass filter coefficient for derivative term
    D_FILTER_BETA = 0.1  # Adjust between 0.1-0.3 (lower = more filtering)

    # Window size for integral calculation (in seconds)
    INTEGRAL_WINDOW = 1.0
    TICK_RATE = 60

    def __init__(self, default_rotation=np.array([0.0, 0.0], dtype=np.float32)):
        super().__init__(tick_rate=self.TICK_RATE)
        self.player = Player()
        self.game_active = SharedArray(topic="game_active", shape=(1,), dtype=np.bool_)
        self.target = self.__init_target(default_rotation)

        self.error = np.array([0.0, 0.0], dtype=np.float32)
        self.error_sum = np.array([0.0, 0.0], dtype=np.float32)
        self.prev_error = np.array([0.0, 0.0], dtype=np.float32)
        self.last_time = time.time()

        # Initialize filtered derivative term
        self.filtered_error_diff = np.zeros(2, dtype=np.float32)

    def run(self):
        while True:
            try:
                if not self.game_active.read():
                    raise SkipTickException
                pid_output = self.__compute_pid()
                self.__move_mouse(pid_output)

            except SkipTickException:
                pass
            except Exception as e:
                logger.error(f"Error moving mouse: {e}")
            finally:
                self.sleep()

    def __init_target(self, default_rotation: np.ndarray):
        self.target = SharedArray(
            topic="mouse_rotation_tgt", shape=(2,), dtype=np.float32
        )
        if np.any(np.isnan(self.target.read())):
            self.target.write(default_rotation)
        return self.target

    def __compute_pid(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        current_rotation = self.player.rotation
        target_rotation = self.target.read()

        self.error = target_rotation - current_rotation
        # Normalize yaw angle error to [-π, π]
        self.error[0] = (self.error[0] + np.pi) % (2 * np.pi) - np.pi

        # Update integral term
        self.error_sum += self.error * dt

        # Calculate derivative term with low-pass filter
        if dt > 1e-4:
            error_diff_raw = (self.error - self.prev_error) / dt
            # Apply low-pass filter to derivative term
            self.filtered_error_diff = (
                self.D_FILTER_BETA * error_diff_raw
                + (1 - self.D_FILTER_BETA) * self.filtered_error_diff
            )
            error_diff = self.filtered_error_diff
        else:
            error_diff = np.zeros(2, dtype=np.float32)

        # Update previous error
        self.prev_error = self.error.copy()

        # Calculate PID terms
        p_term = self.P * self.error
        i_term = self.I * self.error_sum
        d_term = self.D * error_diff

        # Calculate total PID output
        pid_output = p_term + i_term + d_term

        return pid_output

    def __move_mouse(self, control_signal: np.ndarray):
        signal_int = control_signal.astype(np.int32)
        signal_dec = control_signal - signal_int

        # Probabilistic rounding for fractional parts
        dx = signal_int[0] + (signal_dec[0] > np.random.rand())
        dy = signal_int[1] + (signal_dec[1] > np.random.rand())

        pyautogui.move(dx, dy)


if __name__ == "__main__":
    controller = MouseMovementController()
    controller.run()
