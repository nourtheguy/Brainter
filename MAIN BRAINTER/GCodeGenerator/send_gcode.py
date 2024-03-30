# gcode_generator.py
import pyautogui
import pyperclip
import time

input_filepath = "MAIN BRAINTER/GCodeGenerator/Assets/GCode/combined.txt"


def start_automation(input_filepath):
    """
    Opens Universal Gcode Sender, pastes G-code from clipboard, and presses the 'Play' button.
    Adjust mouse coordinates and keystrokes based on your specific setup.
    """
    # Example steps (these need to be customized):
    # Bring UGS to focus or open it

    with open(input_filepath, "r") as input_file:
        content = input_file.read()
        pyperclip.copy(content)

    pyautogui.click(1000, 1050)  # Placeholder: click position to open or focus UGS
    time.sleep(1)

    pyautogui.click(1109, 575)  # Placeholder: click position to open or focus UGS
    time.sleep(1)

    # You might need to click on the text area where G-code is pasted
    pyautogui.position(
        400, 14770
    )  # Placeholder: click position of G-code text area in UGS
    time.sleep(1)
    # Paste the G-code
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.position(715, 53000)
    # Press the "Play" button - this could also be a keyboard shortcut or a precise mouse click
    pyautogui.click(
        715, 53000
    )  # Placeholder: click position of the "Play" button in UGS

    print("G-code should now be running in UGS.")


# start_automation(input_filepath)
