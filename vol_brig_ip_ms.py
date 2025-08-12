from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import speech_recognition
import pyttsx3
import os
import pyautogui
import datetime
import time
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

import screen_brightness_control as sbc

def increase_brightness(amount=10):
    # Increase brightness by a specified amount (default is 10%)
    current_brightness = sbc.get_brightness()[0]  # Get the current brightness level
    new_brightness = min(current_brightness + amount, 100)  # Ensure it doesn't go above 100%
    sbc.set_brightness(new_brightness)
    speak(f"Brightness increased to {new_brightness} percent.")
    print(f"Brightness increased to {new_brightness}%.")

def decrease_brightness(amount=10):
    # Decrease brightness by a specified amount (default is 10%)
    current_brightness = sbc.get_brightness()[0]  # Get the current brightness level
    new_brightness = max(current_brightness - amount, 0)  # Ensure it doesn't go below 0%
    sbc.set_brightness(new_brightness)
    speak(f"Brightness decreased to {new_brightness} percent.")
    print(f"Brightness decreased to {new_brightness}%.")



def mute_volume():
    # Get the default audio device
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Mute the volume
    volume.SetMute(1, None)
    speak("System volume muted.")
    print("System volume muted.")

def unmute_volume():
    # Get the default audio device
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Unmute the volume
    volume.SetMute(0, None)
    speak("System volume unmuted.")
    print("System volume unmuted.")

def open_word():
    speak("Opening Microsoft Word.")
    # Replace with the correct path if Office is installed in a different location
    os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE")
    print("Microsoft Word opened.")

def open_excel():
    speak("Opening Microsoft Excel.")
    # Replace with the correct path if Office is installed in a different location
    os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE")
    print("Microsoft Excel opened.")

def open_powerpoint():
    speak("Opening Microsoft PowerPoint.")
    # Replace with the correct path if Office is installed in a different location
    os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE")
    print("Microsoft PowerPoint opened.")

def close_application(app_name):
    speak(f"Closing {app_name}.")
    # Press Alt + F4 to close the active window
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)  # Pause for a moment to ensure the command is executed
    print(f"{app_name} closed.")