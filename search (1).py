import webbrowser
from googlesearch import search
import speech_recognition as sr
import pyttsx3
import pyautogui




# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice input and recognize speech
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is down. Please try again later.")
        return ""

def close_all_tabs():
    speak("Closing all tabs and the browser.")
    pyautogui.hotkey('alt', 'f4')  # Use 'command' + 'q' instead for Mac

def close_browser_tabs(name):
    # Close the specified browser tabs
    
    speak(f"Closing the {name} tab.")
    pyautogui.hotkey('ctrl', 'w')  # Use 'command' instead of 'ctrl' on Mac

def google_search(query, num_results=10):
    print(f"Searching Google for: {query}\n")
    
    # Perform the search
    results = search(query, num_results=num_results)
    
    # Open the first result
    try:
        first_result = next(results)  # Get the first result
        print(f"Opening the first result: {first_result}\n")
        webbrowser.open(first_result)  # Open the first result in the web browser
    except StopIteration:
        print("No results found.")
        speak("No results found for your search.")

def wikipedia_search(query):
    url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    print(f"Opening Wikipedia page for: {query}\n")
    webbrowser.open(url)

def main():
    speak("Welcome to the voice command search assistant.")
    
    while True:
        speak("Would you like to search a topic on Google, Wikipedia, open Google, open Wikipedia, or exit?")
        command = listen()
        
        if "google" in command and "search" in command:
            topic = command.replace("google search", "").strip()
            if topic:  # Ensure the topic is not empty
                google_search(topic)
            else:
                speak("Please specify a topic to search on Google.")
        elif "wikipedia" in command and "search" in command:
            topic = command.replace("wikipedia search", "").strip()
            if topic:  # Ensure the topic is not empty
                wikipedia_search(topic)
            else:
                speak("Please specify a topic to search on Wikipedia.")
        elif "open google" in command:
            webbrowser.open("https://www.google.com")
            print("Google is now open in your web browser.")
            speak("Google is now open in your web browser.")
        elif "open wikipedia" in command:
            webbrowser.open("https://www.wikipedia.org")
            print("Wikipedia is now open in your web browser.")
            speak("Wikipedia is now open in your web browser.")
        elif "exit" in command or "quit" in command or "stop" in command:
            speak("Exiting the program.")
            break
        else:
            speak("Invalid command, please try again.")

if __name__ == "__main__":
    main()
