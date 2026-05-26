# core/image_recognition.py
import cv2
import numpy as np
from pathlib import Path

class ImageRecognizer:
    """
    Image recognition class using template matching to locate specific UI elements
    such as the skip button, dialog options, or loading completion indicators.
    """
    def __init__(self, templates_dir="assets/templates", confidence=0.8):
        """
        :param templates_dir: Directory containing template images
        :param confidence: Template matching threshold (0~1)
        """
        self.templates = {}
        self.confidence = confidence
        self.templates_dir = Path(templates_dir)
        self._load_templates()

    def _load_templates(self):
        """Pre-load all template images (grayscale)."""
        template_names = ["skip_button", "dialog_option", "loading_finish"]
        for name in template_names:
            path = self.templates_dir / f"{name}.png"
            if path.exists():
                img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    self.templates[name] = img
                else:
                    print(f"Warning: Cannot read template image {path}")
            else:
                print(f"Warning: Template image not found {path}")

    def find_template(self, haystack, template_name):
        """
        Search for a template in the given image.
        :param haystack: np.ndarray, BGR or grayscale
        :param template_name: Template name (filename without extension)
        :return: Center point (x, y) of the matched template, or None if not found
        """
        if template_name not in self.templates:
            return None
        template = self.templates[template_name]
        if haystack is None or template is None:
            return None

        # Convert to grayscale if needed
        if len(haystack.shape) == 3:
            gray = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
        else:
            gray = haystack

        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val >= self.confidence:
            h, w = template.shape
            center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            return center
        return None

    def is_skip_available(self, screenshot):
        """Quick check: is the skip button present?"""
        return self.find_template(screenshot, "skip_button") is not None

    def is_dialog_option(self, screenshot):
        """Check if there is a dialog option (requires pressing F)."""
        return self.find_template(screenshot, "dialog_option") is not None

    def is_loading_finished(self, screenshot):
        """Check if loading is complete (e.g., 'click to continue' appears)."""
        return self.find_template(screenshot, "loading_finish") is not None
