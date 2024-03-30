import pyautogui
import time

while True:
    # Prints the current mouse coordinates
    x, y = pyautogui.position()
    print(f"X: {x}, Y: {y}", end='\r')
    time.sleep(1)  # Sleep for 1 second to make it easier to read
