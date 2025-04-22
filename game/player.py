import time
import pyautogui
import numpy as np
from dds.sharedarray import SharedArray

np.set_printoptions(precision=1, suppress=True)


class Player:
    def __init__(self):
        self.__position_array: SharedArray | None = None
        self.__tile_array: SharedArray | None = None
        self.__rotation_array: SharedArray | None = None
        self.__direction_array: SharedArray | None = None

    @property
    def position(self):
        if self.__position_array is None:
            self.__position_array = SharedArray(
                topic="player_position_now", shape=(3,), dtype=np.float32
            )
        return self.__position_array.read()

    @property
    def tile(self):
        if self.__tile_array is None:
            self.__tile_array = SharedArray(
                topic="player_tile_now", shape=(3,), dtype=np.int32
            )
        return self.__tile_array.read()

    @property
    def rotation(self):
        if self.__rotation_array is None:
            self.__rotation_array = SharedArray(
                topic="player_rotation_now", shape=(2,), dtype=np.float32
            )
        return self.__rotation_array.read()

    @property
    def direction(self):
        if self.__direction_array is None:
            self.__direction_array = SharedArray(
                topic="player_direction_now", shape=(3,), dtype=np.float32
            )
        return self.__direction_array.read()
