import time
import pyautogui
from game.master import MinecraftMaster
import numpy as np
from mcpi.minecraft import Minecraft

np.set_printoptions(precision=1, suppress=True)

class Player:
    def __init__(self, master: MinecraftMaster):
        self.master: MinecraftMaster = master
        self.mc: Minecraft = master.mc
        # Set a very small pause for more responsive movement
        pyautogui.PAUSE = 0.005

    @property
    def pos(self):
        pos = self.mc.player.getPos()
        return np.array([pos.x, pos.y, pos.z])
    
    @property
    def direction(self):
        dir = self.mc.player.getDirection()
        return np.array([dir.x, dir.y, dir.z])
    
    def turn_right(self):
        t0 = time.time()
        while time.time() - t0 < 1.0:
            pyautogui.move(1.0, 0.0, duration=1.0, tween=pyautogui.easeInOutQuad)
    
    def face_direction(self, tgt_roll: float, tgt_pitch: float):
        t0 = time.time()
        
        while time.time() - t0 < 10: 
            if not self.master.is_focused:
                time.sleep(0.1)
                continue
                
            dir = self.direction
            roll = np.arctan2(dir[2], dir[0])
            pitch = np.arctan2(dir[1], np.linalg.norm(dir[[0,2]]))

            # Calculate angle differences
            delta_roll = (roll - tgt_roll + np.pi) % (2 * np.pi) - np.pi
            delta_pitch = pitch - tgt_pitch


            dx = -0.5 if delta_roll > 0 else 0.5
            # dy = -1 if delta_pitch > 0 else 1

            pyautogui.move(dx, 0, duration=0.01)