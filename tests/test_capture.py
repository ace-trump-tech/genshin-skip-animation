# tests/test_capture.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from core.screen_capture import ScreenCapture

def test_screen_capture_initialization():
    """Test ScreenCapture initialization."""
    cap = ScreenCapture()
    assert cap.region is None
    assert cap.sct is not None

def test_screen_capture_set_region():
    """Test setting capture region."""
    cap = ScreenCapture()
    region = {'top': 10, 'left': 20, 'width': 800, 'height': 600}
    cap.set_region(region)
    assert cap.region == region

def test_screen_capture_capture_returns_image():
    """Test that capture returns a numpy array (requires actual screen)."""
    cap = ScreenCapture()
    img = cap.capture()
    # Skip test if running in headless environment
    if img is not None:
        assert isinstance(img, np.ndarray)
        assert len(img.shape) == 3  # height, width, channels
        assert img.shape[2] == 3    # BGR channels
