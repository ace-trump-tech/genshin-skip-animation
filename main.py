# main.py
import sys
import time
import threading
import yaml
from core.state_machine import StateMachine
from utils.logger import setup_logger
from utils.hotkey_listener import HotkeyListener

logger = setup_logger()

def main():
    # Load configuration
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # Set log level from config
    logger.setLevel(getattr(logging, config.get("log_level", "INFO").upper()))

    # Initialize state machine and hotkey listener
    sm = StateMachine(config)
    hotkey = HotkeyListener(config)

    # Define hotkey callbacks
    def on_start():
        logger.info("Auto-skip started")
        sm.start()

    def on_stop():
        logger.info("Auto-skip stopped")
        sm.stop()

    hotkey.on_start = on_start
    hotkey.on_stop = on_stop
    hotkey.start()

    logger.info(f"Press {config['hotkey_start']} to start, {config['hotkey_stop']} to stop")
    logger.info("Press Ctrl+C to exit")

    # Keep main thread alive
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info("Exiting...")
        sm.stop()
        sys.exit(0)

if __name__ == "__main__":
    import logging  # for setLevel in main()
    main()
