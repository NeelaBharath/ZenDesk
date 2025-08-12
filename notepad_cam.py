import speech_recognition as sr
import pyttsx3
import os
import subprocess
import time
import cv2
import pyautogui
import datetime
import webbrowser
# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for background noise
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()  # Return recognized command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat?")
        return ""
    except sr.RequestError:
        speak("Could not request results; check your internet connection.")
        return ""
    


def take_screenshot():
    # Generate a filename with the current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    directory = r"C:\Users\saanv\OneDrive\Pictures\Screenshots"
    filename = os.path.join(directory, f"screenshot_{timestamp}.png")
    
    # Check if the directory exists; if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory if it doesn't exist
    
    # Take the screenshot
    screenshot = pyautogui.screenshot()
    
    # Save the screenshot to the specified file
    screenshot.save(filename)

# Function to open Notepad
def open_notepad():
    speak("Opening Notepad.")
    # Open Notepad
    subprocess.Popen("C:\\Windows\\notepad.exe")
    time.sleep(2)  # Wait for Notepad to open
#write a python code to open and then take notes in notepad and then save the file and then close the notepad
#take the file name from user and then save the file with that name

def parse_time(time_string):
    try:
        alarm_time = datetime.datetime.strptime(time_string, "%I:%M %p")
        # Set the alarm date to today
        now = datetime.datetime.now()
        alarm_time = alarm_time.replace(year=now.year, month=now.month, day=now.day)
        
        # If alarm time is in the past, set for the next day
        if alarm_time < now:
            alarm_time += datetime.timedelta(days=1)
        return alarm_time
    except ValueError:
        return None

# Function to set the alarm
def set_alarm():
    speak("What time would you like to set the alarm for? Please say the time in the format, for example, '7 30 PM'.")
    alarm_time_str = take_command()
    
    if not alarm_time_str:
        speak("I couldn't understand the time. Please try again.")
        return
    
    alarm_time = parse_time(alarm_time_str)
    if not alarm_time:
        speak("The time format seems incorrect. Please try again.")
        return
    
    speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}")
    
    # Wait until the alarm time
    while datetime.datetime.now() < alarm_time:
        time.sleep(1)
    
    # Ring the alarm
    speak("Time's up! This is your alarm.")

def open_camera():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        speak("I couldn't access the camera. Please ensure it's connected and not in use.")
        return
    
    while True:
        ret, img = cap.read()
        
        # Check if frame was captured
        if not ret:
            print("Error: Failed to capture image.")
            speak("I couldn't capture the image. There may be an issue with the camera.")
            break
        
        cv2.imshow('webcam', img)
        
        # Break on 'Esc' key press
        if cv2.waitKey(50) == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()

def close_camera():
    global camera_active
    if camera_active:
        camera_active = False  # Set the flag to False to stop the camera loop
        speak("Closing the camera.")

def take_notes(save_path):
    # Ask for the file name
    speak("What would you like to name your notes file?")
    file_name = take_command().replace(" ", "_")  # Replace spaces with underscores for the file name
    full_file_name = f"{file_name}.txt"  # Add the .txt extension

    # Open Notepad
    speak("Opening Notepad to take notes.")
    open_notepad()

    # Capture voice input until "stop" is said
    speak("Please start speaking. Say 'stop' to save and close the notes.")
    notes = ""
    while True:
        command = take_command()
        if "stop" in command:
            break
        notes += command + "\n"  # Add each line of input as a new line

    # Save the notes in the specified path
    file_path = os.path.join(save_path, full_file_name)
    with open(file_path, "w") as file:
        file.write(notes)

    # Type the saved notes into Notepad
    time.sleep(1)  # Wait for Notepad to settle
    pyautogui.hotkey("ctrl", "a")  # Select all existing text in Notepad
    pyautogui.press("backspace")  # Clear existing text
    time.sleep(0.5)  # Wait a moment before typing
    pyautogui.typewrite(notes)  # Type the notes into Notepad
    speak(f"Notes have been saved at {file_path}.")

    # Optionally, close Notepad
    time.sleep(1)  # Wait before closing
    pyautogui.hotkey("alt", "f4")  # Close Notepad
    pyautogui.press("right")  # Confirm "Don't Save" if prompted
    pyautogui.press("enter")
    


def click_photo():
    speak("Opening camera to take a photo.")
    cap = cv2.VideoCapture(0)  # Open the default camera

    if not cap.isOpened():
        speak("Could not open the camera.")
        return

    ret, frame = cap.read()  # Capture a frame
    if ret:
        # Save the captured image to the current directory
        filename = f"photo_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        speak(f"Photo has been taken and saved as {filename}.")
    else:
        speak("Failed to capture the photo.")

    cap.release()  # Release the camera
    cv2.destroyAllWindows()

def open_edge():
    # Using subprocess to open Microsoft Edge
    try:
        # This will open Microsoft Edge
        subprocess.Popen("msedge.exe")
        print("Microsoft Edge has been opened.")
    except FileNotFoundError:
        print("Microsoft Edge is not found. Please ensure it is installed and in the system path.")

def close_notepad():
    speak("Closing Notepad.")
    # Use taskkill to close Notepad on Windows
    os.system("taskkill /f /im notepad.exe")

def get_location(prompt_text):
    while True:
        speak(prompt_text)
        location = take_command()
        if location:
            return location
        else:
            speak("I couldn't understand the location. Please try again.")

def open_google_maps():
    # Get current location and destination through voice input
    current_location = get_location("Please say your current location.")
    destination = get_location("Please say your destination.")

    # Construct the Google Maps URL
    base_url = "https://www.google.com/maps/dir/"
    maps_url = f"{base_url}{current_location}/{destination}"

    # Open Google Maps with the specified directions
    speak(f"Opening Google Maps for directions from {current_location} to {destination}.")
    webbrowser.open(maps_url)

# Main function to execute the tasks
def main():
    speak("Welcome. I am your voice assistant.")
    while True:
        speak("How can I assist you?")
        command = take_command()

        if "open notepad" in command:
            open_notepad()
        elif "take notes" in command:
            downloads_path = r"C:\Users\saanv\Downloads"  # Replace <YourUsername> with your actual username
            take_notes(downloads_path)
        elif "close notes" in command or "close notepad" in command:
            take_notes()
        elif "open browser" in command:
            open_edge()
        elif "exit" in command or "quit" in command or "stop" in command:
            speak("Goodbye!")
            break
        else:
            speak("I didn't understand that command. Please try again.")

if __name__ == "__main__":
    main()
