# tests/test_recognition.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import numpy as np
from core.image_recognition import ImageRecognizer

def test_image_recognizer_loads_templates():
    """Test that recognizer loads templates from directory."""
    # Use dummy templates directory (you may need to create one for testing)
    # For this test, we'll assume the default assets/templates exists.
    # Alternatively, we can mock the loading.
    rec = ImageRecognizer(templates_dir="assets/templates", confidence=0.8)
    # Even if no templates exist, the object should be created without crash
    assert rec.templates is not None

def test_find_template_not_found():
    """Test find_template returns None when template is absent."""
    rec = ImageRecognizer(templates_dir="assets/templates", confidence=0.8)
    # Create a dummy screenshot
    screenshot = np.zeros((100, 100, 3), dtype=np.uint8)
    result = rec.find_template(screenshot, "non_existent")
    assert result is None

def test_find_template_with_dummy():
    """Test template matching with a dummy template and screenshot."""
    # Create a recognizer with confidence 1.0
    rec = ImageRecognizer(templates_dir="assets/templates", confidence=1.0)
    # Manually inject a dummy template
    template = np.ones((10, 10), dtype=np.uint8) * 255
    rec.templates["dummy"] = template
    # Create screenshot that contains the template
    screenshot = np.zeros((100, 100, 3), dtype=np.uint8)
    # Place template at (20,20) in grayscale then convert to BGR
    gray_screen = np.zeros((100, 100), dtype=np.uint8)
    gray_screen[20:30, 20:30] = 255
    # Convert to BGR for find_template
    bgr_screen = cv2.cvtColor(gray_screen, cv2.COLOR_GRAY2BGR)
    pos = rec.find_template(bgr_screen, "dummy")
    # Expected center: (20+10//2, 20+10//2) = (25,25)
    assert pos == (25, 25)
