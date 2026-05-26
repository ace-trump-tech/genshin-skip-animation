# core/screen_capture.py
import mss
import numpy as np

class ScreenCapture:
    """
    Screen capture class. Supports capturing full screen or a specified region.
    Returns image in OpenCV format (BGR) as numpy array.
    """
    def __init__(self, region=None):
        """
        :param region: capture region in mss format {'top': y, 'left': x, 'width': w, 'height': h}
                       None means capture the primary monitor.
        """
        self.sct = mss.mss()
        self.region = region

    def capture(self):
        """
        Capture current screen content.
        :return: np.ndarray, shape (height, width, 3), color channel BGR
        """
        monitor = self.region if self.region else self.sct.monitors[1]
        img = self.sct.grab(monitor)
        # mss returns BGRA, convert to BGR by removing alpha channel
        return np.array(img)[:, :, :3]

    def set_region(self, region):
        """Dynamically change the capture region."""
        self.region = region
