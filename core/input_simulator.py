# core/input_simulator.py
import pyautogui
import time
import random

class InputSimulator:
    """
    Simulate keyboard and mouse input with random delays to reduce detection risk.
    """
    def __init__(self, min_delay=0.05, max_delay=0.15):
        """
        :param min_delay: Minimum delay after each action (seconds)
        :param max_delay: Maximum delay after each action (seconds)
        """
        pyautogui.FAILSAFE = False   # Disable the corner emergency stop
        self.min_delay = min_delay
        self.max_delay = max_delay

    def _random_delay(self):
        time.sleep(random.uniform(self.min_delay, self.max_delay))

    def click(self, x, y):
        """Simulate left mouse click at (x, y)."""
        pyautogui.click(x, y)
        self._random_delay()

    def press_key(self, key):
        """Simulate a key press (e.g., 'f', 'space', 'enter')."""
        pyautogui.press(key)
        self._random_delay()

    def move_to(self, x, y, duration=0.2):
        """Smoothly move mouse to (x, y)."""
        pyautogui.moveTo(x, y, duration=duration)
        self._random_delay()
