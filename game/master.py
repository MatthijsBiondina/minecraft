from mcpi.minecraft import Minecraft
import pyautogui

import time

from utils.tools import get_active_window_title

class MinecraftMaster:
    def __init__(self):
        self.mc = Minecraft.create("localhost")

    @property
    def is_focused(self):
        window = get_active_window_title()
        return "Multiplayer (3rd-party Server)" in window

        

    def focus(self):
        # press windows key
        pyautogui.press("win")
        time.sleep(0.1)
        pyautogui.write("Minecraft")
        time.sleep(0.2)
        pyautogui.press("enter")
        time.sleep(0.5)
        pyautogui.moveTo(1920 // 2, 364, duration=1.0, tween=pyautogui.easeInQuad)
        time.sleep(0.5)
        pyautogui.click()
