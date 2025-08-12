import webbrowser
import pyautogui
import speech_recognition as sr
import pyttsx3

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

# Function to open YouTube
def open_youtube():
    webbrowser.open("https://www.youtube.com")
    speak("YouTube is now open in your web browser.")

def open_youtube_with_topic(topic):
    search_url = f"https://www.youtube.com/results?search_query={topic.replace(' ', '+')}"
    webbrowser.open(search_url)
    speak(f"Opening YouTube with the topic {topic}.")

# Function to close YouTube
def close_youtube():
    speak("Closing YouTube and the browser.")
    pyautogui.hotkey('alt', 'f4')  # Use 'command' + 'q' instead for Mac

def main():
    speak("Welcome to the voice command assistant.")

    while True:
        speak("What topic would you like to search for on YouTube? Say 'open YouTube with topic' followed by your topic, or say 'exit' to quit.")
        command = listen()

        if "open youtube with" in command:
            topic = command.replace("open youtube with", "").strip()  # Extract topic from command
            if topic:
                open_youtube_with_topic(topic)
            else:
                speak("Please specify a topic to search on YouTube.")
        elif "open youtube" in command and "with" not in command:
            open_youtube()  # Open the main YouTube page
        elif "close youtube" in command:
            close_youtube()
        elif "exit" in command or "quit" in command or "stop" in command:
            speak("Exiting the program.")
            break
        else:
            speak("Invalid command, please try again.")

if __name__ == "__main__":
    main()
