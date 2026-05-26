# core/state_machine.py
import time
import threading
from core.screen_capture import ScreenCapture
from core.image_recognition import ImageRecognizer
from core.input_simulator import InputSimulator

class StateMachine:
    """
    Main state machine: continuously captures screen, recognizes UI elements,
    and triggers corresponding simulated actions.
    """
    def __init__(self, config):
        """
        :param config: Configuration dictionary with keys:
            - capture_region: screenshot region (None or dict)
            - confidence: recognition confidence threshold
            - skip_wait_after: wait time after clicking skip button
            - loop_interval: main loop interval (seconds)
        """
        self.running = False
        self.config = config
        self.capture = ScreenCapture(config.get("capture_region"))
        self.recognizer = ImageRecognizer(
            templates_dir="assets/templates",
            confidence=config.get("confidence", 0.8)
        )
        self.simulator = InputSimulator()
        self.thread = None

    def start(self):
        """Start the auto-skip loop (non-blocking)."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop the auto-skip loop."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)

    def _loop(self):
        """Main loop: capture -> recognize -> act."""
        interval = self.config.get("loop_interval", 0.3)
        while self.running:
            screenshot = self.capture.capture()

            # 1. Priority: skip button
            skip_pos = self.recognizer.find_template(screenshot, "skip_button")
            if skip_pos:
                self.simulator.click(*skip_pos)
                wait = self.config.get("skip_wait_after", 1.0)
                time.sleep(wait)
                continue   # re-capture after waiting

            # 2. Dialog option: press F to continue
            if self.recognizer.is_dialog_option(screenshot):
                self.simulator.press_key("f")
                time.sleep(0.2)
                continue

            # 3. Loading finished: click screen center
            if self.recognizer.is_loading_finished(screenshot):
                h, w = screenshot.shape[:2]
                self.simulator.click(w // 2, h // 2)
                time.sleep(0.5)
                continue

            # No actionable element found, sleep briefly
            time.sleep(interval)
