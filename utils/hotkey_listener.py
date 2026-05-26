# utils/hotkey_listener.py
from pynput import keyboard

class HotkeyListener:
    """
    Global hotkey listener using pynput.
    Detects key combinations and triggers callbacks.
    """

    def __init__(self, config):
        """
        :param config: Configuration dict containing 'hotkey_start' and 'hotkey_stop' keys.
                       Each hotkey should be a string like "ctrl+shift+s" or "ctrl+shift+x".
        """
        self.start_hotkey = self._parse_hotkey(config["hotkey_start"])
        self.stop_hotkey = self._parse_hotkey(config["hotkey_stop"])
        self.on_start = None   # Callback to be set externally
        self.on_stop = None    # Callback to be set externally
        self.current_keys = set()
        self.listener = None

    def _parse_hotkey(self, hotkey_str):
        """
        Parse a hotkey string like "ctrl+shift+s" into a list of normalized key strings.
        """
        parts = hotkey_str.lower().split('+')
        normalized = []
        for p in parts:
            p = p.strip()
            if p == 'ctrl':
                normalized.append('ctrl')
            elif p == 'shift':
                normalized.append('shift')
            elif p == 'alt':
                normalized.append('alt')
            elif p == 'cmd' or p == 'win':
                normalized.append('cmd')
            else:
                # single character key (e.g., 's', 'x')
                normalized.append(p)
        return normalized

    def _normalize_key(self, key):
        """
        Convert a pynput key object to a string representation.
        """
        try:
            # Regular character key
            return key.char.lower()
        except AttributeError:
            # Special key (ctrl, shift, alt, etc.)
            key_name = str(key).replace('Key.', '').lower()
            return key_name

    def _on_press(self, key):
        k = self._normalize_key(key)
        self.current_keys.add(k)
        self._check_hotkeys()

    def _on_release(self, key):
        k = self._normalize_key(key)
        if k in self.current_keys:
            self.current_keys.remove(k)

    def _check_hotkeys(self):
        # Check if all keys in start_hotkey are currently pressed
        if all(k in self.current_keys for k in self.start_hotkey):
            if self.on_start:
                self.on_start()
        # Check stop hotkey
        elif all(k in self.current_keys for k in self.stop_hotkey):
            if self.on_stop:
                self.on_stop()

    def start(self):
        """Start listening for global hotkeys (non-blocking)."""
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()

    def stop(self):
        """Stop the listener."""
        if self.listener and self.listener.is_alive():
            self.listener.stop()
