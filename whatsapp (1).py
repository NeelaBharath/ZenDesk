import pywhatkit as kit
import speech_recognition as sr
import pyttsx3
import os
import platform
import time

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands
def take_command():
    while True:  # Loop until a valid command is recognized
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
                print("Sorry, I didn't catch that. Could you repeat?")
                speak("Sorry, I didn't catch that. Could you repeat?")
            except sr.RequestError:
                print("Could not request results; check your internet connection.")
                speak("Could not request results; check your internet connection.")

# Function to open WhatsApp Web
def open_whatsapp():
    speak("Opening WhatsApp.")
    if platform.system() == "Windows":
        os.startfile("https://web.whatsapp.com/")
    elif platform.system() == "Darwin":  # macOS
        os.system("open https://web.whatsapp.com/")
    else:  # Linux
        os.system("xdg-open https://web.whatsapp.com/")
    time.sleep(5)  # Wait for the page to load

# Function to close the browser
def close_whatsapp():
    speak("Closing WhatsApp.")
    if platform.system() == "Windows":
        os.system("taskkill /f /im chrome.exe")  # Change to your browser's executable if needed
    elif platform.system() == "Darwin":  # macOS
        os.system("pkill -f 'Google Chrome'")
    else:  # Linux
        os.system("pkill -f 'chrome'")  # Change to your browser's executable if needed

# Mapping contact names to phone numbers (without country code)
contacts = {
    "Shiny": "9177398358",
    "Sneha": "9494780049",
    "John": "7780219966",
    "bharath":"7032639047"
}

# Main function to send a WhatsApp message instantly
from difflib import get_close_matches

# Function to find the closest match for a contact name
def find_contact(name):
    possible_matches = get_close_matches(name, contacts.keys(), n=1, cutoff=0.6)  # Cutoff can be adjusted
    if possible_matches:
        return contacts[possible_matches[0]]
    return None

# Main function to send a WhatsApp message instantly
def send_whatsapp_message():
    speak("Do you want to open WhatsApp first? Say 'yes' or 'no'.")
    open_decision = take_command()
    if open_decision == "yes" or "s":
        open_whatsapp()

    speak("To whom do you want to send a WhatsApp message?")
    contact_name = take_command()
    contact_number = find_contact(contact_name)

    if not contact_number:
        speak("I couldn't find that contact. Please ensure the contact is in the list.")
        print(f"Recognized name: {contact_name} not found in contacts.")  # Debugging output
        return

    # Adding the default country code for India if not provided
    if not contact_number.startswith("+"):
        contact_number = "+91" + contact_number

    speak("What message would you like to send?")
    message = take_command()

    # Sending the message instantly using pywhatkit
    speak(f"Sending message to {contact_name}.")
    try:
        time.sleep(5)  # Ensure there's enough time for WhatsApp Web to load
        kit.sendwhatmsg_instantly(contact_number, message, 15)  # Specify delay in seconds if needed
        speak("Message has been sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, I couldn't send the message.")

    speak("Do you want to close WhatsApp now? Say 'yes' or 'no'.")
    close_decision = take_command()
    if close_decision == "yes":
        close_whatsapp()


# Run the assistant
if __name__ == "__main__":
    speak("Welcome. I am your voice assistant.")
    while True:
        speak("How can I assist you?")
        command = take_command()
        
        # Handling different commands
        if "send whatsapp message" in command:
            send_whatsapp_message()
        elif "open whatsapp" in command:
            open_whatsapp()
        elif "close whatsapp" in command:
            close_whatsapp()
        elif "exit" in command or "stop" in command or "quit" in command:
            speak("Goodbye!")
            break
        else:
            speak("I didn't understand that command. Please try again.")

