from mcpi.minecraft import Minecraft
import time

import numpy as np
from daemons.daemon import Daemon
from dds.sharedarray import SharedArray
from utils.logger import Logger

logger = Logger(__name__)


class PlayerState(Daemon):
    def __init__(self):
        super().__init__(tick_rate=100)
        self.mc = Minecraft.create("localhost")

        self.player_position = SharedArray(
            topic="player_position_now", shape=(3,), dtype=np.float32
        )
        self.player_tile = SharedArray(
            topic="player_tile_now", shape=(3,), dtype=np.int32
        )
        self.player_rotation = SharedArray(
            topic="player_rotation_now", shape=(2,), dtype=np.float32
        )
        self.player_direction = SharedArray(
            topic="player_direction_now", shape=(3,), dtype=np.float32
        )

    def run(self):
        while True:
            try:
                self.__publish_player_pos()
                self.__publish_player_tile()
                self.__publish_player_rotation()
                self.__publish_player_direction()
            except Exception as e:
                logger.error(f"Error getting player position: {e}")
            finally:
                self.sleep()

    def __publish_player_pos(self):
        player_pos = self.mc.player.getPos()
        player_pos = np.array(
            [player_pos.x, player_pos.y, player_pos.z], dtype=np.float32
        )
        self.player_position.write(player_pos)

    def __publish_player_tile(self):
        player_tile = self.mc.player.getTilePos()
        player_tile = np.array(
            [player_tile.x, player_tile.y, player_tile.z], dtype=np.int32
        )
        self.player_tile.write(player_tile)

    def __publish_player_rotation(self):
        player_direction = self.mc.player.getDirection()

        player_rotation = np.array(
            [
                np.arctan2(player_direction.x, player_direction.z),
                np.arctan2(
                    player_direction.y,
                    np.sqrt(player_direction.x**2 + player_direction.z**2),
                ),
            ],
            dtype=np.float32,
        )

        self.player_rotation.write(player_rotation)

    def __publish_player_direction(self):
        player_direction = self.mc.player.getDirection()
        player_direction = np.array(
            [player_direction.x, player_direction.y, player_direction.z],
            dtype=np.float32,
        )
        self.player_direction.write(player_direction)


if __name__ == "__main__":
    player_state = PlayerState()
    player_state.run()
