# tests/test_simulator.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.input_simulator import InputSimulator
import pyautogui
from unittest.mock import patch

def test_input_simulator_initialization():
    """Test InputSimulator initialization."""
    sim = InputSimulator(min_delay=0.01, max_delay=0.02)
    assert sim.min_delay == 0.01
    assert sim.max_delay == 0.02

@patch('pyautogui.click')
@patch('time.sleep')
def test_click(mock_sleep, mock_click):
    """Test click method calls pyautogui.click."""
    sim = InputSimulator(min_delay=0.0, max_delay=0.0)
    sim.click(100, 200)
    mock_click.assert_called_once_with(100, 200)
    mock_sleep.assert_called_once()

@patch('pyautogui.press')
@patch('time.sleep')
def test_press_key(mock_sleep, mock_press):
    """Test press_key method calls pyautogui.press."""
    sim = InputSimulator(min_delay=0.0, max_delay=0.0)
    sim.press_key('f')
    mock_press.assert_called_once_with('f')
    mock_sleep.assert_called_once()

@patch('pyautogui.moveTo')
@patch('time.sleep')
def test_move_to(mock_sleep, mock_moveTo):
    """Test move_to method calls pyautogui.moveTo."""
    sim = InputSimulator(min_delay=0.0, max_delay=0.0)
    sim.move_to(300, 400, duration=0.5)
    mock_moveTo.assert_called_once_with(300, 400, duration=0.5)
    mock_sleep.assert_called_once()
