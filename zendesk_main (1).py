import speech_recognition as sr
import pyttsx3
from search import *
from whatsapp import *
from youtube import *
from mailing import *
from notepad_cam import *
import cv2
import pyautogui
import threading
import requests
import psutil
from vol_brig_ip_ms import *
import speedtest
from bs4 import BeautifulSoup
import pygetwindow as gw
import os
import smtplib
from email.mime.text import MIMEText
import requests
# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice input and recognize speech using Google Web Speech API
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Recognize speech using Google's Web Speech API
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is down. Please try again later.")
        return ""

def wait_for_load(seconds=7):
    time.sleep(seconds)

def news():
    kit.playonyt("https://www.youtube.com/watch?v=Jw0FZJzK2Xc")
    speak("Here is the latest news from India")
    wait_for_load()
    speak("Do you want to search for any other news?")
    query = take_command().lower()
    if 'yes' in query:
        speak("What do you want to search for?")
        query = take_command().lower()
        kit.playonyt(query)
    else:
        speak("Thank you for using Zen")
        exit()

# Function to perform tasks based on the command
def execute_task(command):
    if "who are you" in command or "who you" in command:
        speak("I am Zen, your personal assistant.")
    elif "google search" in command:
        topic = command.replace("google search", "").strip()
        google_search(topic)
    elif "wikipedia search" in command:
        topic = command.replace("wikipedia search", "").strip()
        wikipedia_search(topic)
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        print("Google is now open in your web browser.")
        speak("Google is now open in your web browser.")
    elif "open wikipedia" in command:
        webbrowser.open("https://www.wikipedia.org")
        print("Wikipedia is now open in your web browser.")
        speak("Wikipedia is now open in your web browser.")  
    elif "close google" in command:
        close_browser_tabs("Google")
    elif 'battery percentage' in command or 'show percentage' in command or 'battery' in command:
        battery = psutil.sensors_battery()  # Get battery status
        if battery:
            percent = battery.percent  # Get battery percentage
            is_plugged = battery.power_plugged  # Check if charging
            if is_plugged:
                speak(f"The battery is charging at {percent} percent.")
            else:
                speak(f"The battery is at {percent} percent.")
        else:
            speak("I am unable to check the battery status.")
    elif "close wikipedia" in command:
        close_browser_tabs("Wikipedia") 
    elif "close all tabs" in command:
        close_all_tabs()
    elif 'open new window' in command or 'open new tab' in command:
        time.sleep(1)
        pyautogui.hotkey('ctrl','n')
    elif 'open incognito window' in command or 'open incognito tab' in command:
        time.sleep(1)
        pyautogui.hotkey('ctrl','shift','n')
    elif 'minimise this window' in command or 'minimise the window' in command or 'minimise window' in command:
        time.sleep(1)
        pyautogui.hotkey('alt','space')
        time.sleep(1)               
        pyautogui.press('n')
    elif 'open history' in command:
        time.sleep(1)
        pyautogui.hotkey('ctrl','h')
    elif 'open downloads' in command:
        time.sleep(1)
        pyautogui.hotkey('ctrl','j')

    elif 'zoom in' in command or 'increase zoom' in command or 'zoomin' in command or 'zoomIn' in command:
        for _ in range(5):  # Adjust the number of times to zoom in
            pyautogui.hotkey('ctrl', '+')  # Simulate pressing Ctrl and +

    elif 'zoom out' in command or 'decrease zoom' in command or 'zoomout' in command:
        for _ in range(5):  # Adjust the number of times to zoom out
            pyautogui.hotkey('ctrl', '-')
    elif 'maximise this window' in command or 'maximise the window' in command or 'maximise window' in command or 'maximize this window' in command or 'maximize thw window' in command:
        pyautogui.hotkey('alt','space')
        time.sleep(1)
        pyautogui.press('x')
    elif 'close tab' in command:
        pyautogui.hotkey('ctrl','w')
    elif 'next tab' in command:
        pyautogui.hotkey('ctrl','tab')
    elif 'close browser' in command:
        os.system("taskkill /f /im msedge.exe")
    elif "open youtube" in command and "with" not in command:
            open_youtube()  # Open the main YouTube page
    elif "close youtube" in command:
        close_browser_tabs("Youtube")
    elif "open youtube with" in command:
        topic = command.replace("open youtube with", "").strip()
        if topic:
            open_youtube_with_topic(topic)
        else:
            speak("Please specify a topic to search on YouTube.")
    elif "who created you" in command or "who made you" in command:
        speak("I was created by Team-15.")
    elif "send whatsapp message" in command or "send a whatsapp message" in command:
        send_whatsapp_message()
    elif "open whatsapp" in command:
        open_whatsapp()
    elif "close whatsapp" in command:
        close_whatsapp()
    
    elif "email" in command or "send an email" in command:
        send_email_command()
    elif "open notepad" in command or "open notes" in command:
        open_notepad()
    elif 'note down' in command or 'take notes' in command:
        file_path = r'C:\Users\saanv\Downloads\sample.txt'
        speak("what should i write")
        note=take_command()
        with open(file_path, 'w') as file:  # Use 'with' to automatically handle file closing
            file.write(note)
    elif 'show notes' in command:
        speak("showing notes")
        file_path = r'C:\Users\saanv\Downloads\sample.txt'
        if os.path.exists(file_path):  # Check if the file exists
            with open(file_path, 'r') as file:
                notes = file.read()
                print(notes)
                speak(notes)
        else:
            speak("No notes found.")
    elif 'shut down the system' in command or 'shut down' in command or 'shutdown' in command:
        os.system("shutdown /s /t 5")
    elif "take screenshot" in command or "take a screenshot" in command or 'screenshot' in command:
        take_screenshot()
    elif 'restart the system' in command or 'restart' in command:
        os.system("shutdown /r /t 5")
    elif 'lock the system' in command or 'lock' in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif 'hibernate the system' in command or 'hibernate' in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif 'sleep the system' in command or 'keep in sleep' in command or 'sleep' in command:
        speak("alright then,I am switching off")
        os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
    elif 'open paint' in command:
        subprocess.Popen("mspaint.exe")
        time.sleep(2)
    elif 'todays news' in command or 'todays news' in command or "today's news" in command or 'news' in command:
        news()
    elif 'close paint' in command:
        os.system("taskkill /f /im mspaint.exe")
    elif 'click photo' in command or 'take photo' in command:
        click_photo()
    elif 'open camera' in command or 'camera open' in command:
        open_camera() 
    elif 'close camera' in command:
        close_camera()
    elif 'what is my ip address' in command or 'what is my IP address' in command or 'tell my ip address' in command or 'IP address' in command or 'ip address' in command:
        speak("Checking...")
        try:
            ipadd = requests.get('https://api.ipify.org').text
            print(ipadd)
            speak("Your IP address is " + ipadd)
        except Exception as e:
            print(e)  # Optionally print the error for debugging
            speak("Network is weak, please try again sometime later.")
    elif 'volume up' in command or 'increase volume' in command or 'increase sound' in command or 'up volume'in command or 'sound increase' in command:
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
        pyautogui.press("volumeup")
    elif 'volume down' in command or 'decrease volume' in command or 'decrease sound' in command or 'down volume'in command:
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
        pyautogui.press("volumedown")
    elif "increase brightness" in command:
        increase_brightness()
    elif "decrease brightness" in command:
        decrease_brightness()
    elif "mute" in command or "mute volume" in command:
        pyautogui.press("volumemute")
    elif "unmute" in command or "unmute volume" in command or 'Unmute' in command:
        pyautogui.press("volumemute")
        
    elif "exit" in command or "quit" in command or "stop" in command:
        speak("Goodbye!")
        return True  # Indicate to stop the program
    elif "open ms word" in command or "open word" in command:
        open_word()
    elif "open ms excel" in command or "open excel" in command:
        open_excel()
    elif "open ms powerpoint" in command or "open powerpoint" in command:
        open_powerpoint()
    elif 'open instagram' in command or 'open Instagram' in command:
        speak("Opening Instagram for you.")
        webbrowser.open("https://www.instagram.com")
    elif 'previous tab' in command.lower():
        pyautogui.hotkey('ctrl','shift','tab')
    elif 'closing browsing history' in command.lower():
        pyautogui.hotkey('ctrl','shift','delete')
    elif 'open command prompt' in command:
        speak("Opening Command Prompt")
        os.system('start cmd')
    elif 'close command prompt' in command:
        speak("Closing Command Prompt")
        os.system('taskkill /f /im cmd.exe')
    elif 'open netflix' in command or 'open Netflix' in command:
        webbrowser.open("https://www.netflix.com")
    elif 'open aaha' in command or 'open aha' in command:
        webbrowser.open("https://www.aaha.video")
    elif 'open prime' in command:
        webbrowser.open("https://www.primevideo.com")
    elif 'open zee5' in command:
        webbrowser.open("https://www.zee5.com")
    elif 'open hotstar' in command:
        webbrowser.open("https://www.hotstar.com")
    elif 'temperature' in command:
        search = 'weather in hyderabad'
        url = f"https://www.google.com/search?q={search}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers)
        data = BeautifulSoup(r.text, "html.parser")
        temp = data.find("span", {"class": "wob_t"}).text
        speak(f"current temperature in Hyderabad is {temp}°C")
        print(f"current temperature in Hyderabad is {temp}°C")
    elif 'internet speed' in command.lower():
        try:
            st = speedtest.Speedtest()  # Initialize the Speedtest object
            speak("Checking internet speed. Please wait...")
            st.get_best_server()  # Find the best server for testing
            dl = st.download()  # Get download speed
            up = st.upload()  # Get upload speed
            speak(f"Your download speed is {dl / 1_000_000:.2f} Mbps and upload speed is {up / 1_000_000:.2f} Mbps.")
        except Exception as e:
            print(e)
            speak("I encountered an issue while trying to check the internet speed.")

    elif "set alarm" in command:
        set_alarm()
    elif "google maps" in command:
        open_google_maps()
    elif 'time' in command or 'current time' in command or 'what is the time' in command:
        current_time = datetime.now().strftime("%I:%M %p")  # Example: "02:30 PM"
        speak(f"The current time is {current_time}")
        print(f"The current time is {current_time}")
    elif 'just open chat' in command or 'launch chatgpt' in command or 'just open chatgpt' in command:
        chatgpt_url = "https://chat.openai.com/"
        speak("Opening ChatGPT")
        webbrowser.open(chatgpt_url) 
    elif 'open chat' in command or 'open chatgpt' in command or 'open ai' in command or 'open chart' in command:
        speak("What would you like to search on ChatGPT?")
        search_query = take_command().lower()  # Capture the search query
        webbrowser.open("https://chat.openai.com/")  # Open ChatGPT's website
        time.sleep(5)  # Give the browser time to load
        if search_query:
            speak(f"Searching for {search_query} on ChatGPT.")
            pyautogui.click()  # Click to focus on the webpage
            time.sleep(1)  # Small delay to ensure everything is ready
            pyautogui.write(search_query, interval=0.1)  # Type the search query
            pyautogui.press("enter")  # Press Enter to submit the search
        else:
            speak("I didn't catch the search query.")
    elif 'close aaha' in command:
        aaha_window = None
        for window in gw.getAllTitles():  # Loop through all open window titles
            if "Aha" in window:  # Check for the Aha tab/window
                aaha_window = gw.getWindowsWithTitle(window)[0]
                break
            if aaha_window:
                aaha_window.close()  # Close only the Aha window

    elif 'close netflix' in command:
        netflix_window = None
        for window in gw.getAllTitles():
            if "Netflix" in window.lower() or "netflix" in window.lower():  # Check for the Netflix tab/window
                netflix_window = gw.getWindowsWithTitle(window)[0]
                break
            if netflix_window:
                netflix_window.close()  # Close only the Netflix window

    elif 'close zee5' in command:
        zee5_window = None
        for window in gw.getAllTitles():
            if "zee5" in window:  # Check for the Zee5 tab/window
                zee5_window = gw.getWindowsWithTitle(window)[0]
                break

            if zee5_window:
                zee5_window.close()  # Close only the Zee5 window
    elif 'open twitter' in command:
        webbrowser.open("https://www.twitter.com")
    elif 'close twitter' in command:
        twitter_window = None
        for window in gw.getAllTitles():
            if "twitter" in window:  # Check for the Twitter tab/window
                    twitter_window = gw.getWindowsWithTitle(window)[0]
                    break
            if twitter_window:
                twitter_window.close() 
    elif 'open github' in command:
            webbrowser.open("https://www.github.com")
    elif 'close github' in command:
        github_window = None
        for window in gw.getAllTitles():  # Loop through all open window titles
            if "GitHub" in window:  # Check if the title contains "GitHub"
                    github_window = gw.getWindowsWithTitle(window)[0]
                    break
            if github_window:
                    github_window.close()  
    elif 'send sms' in command.lower():
        speak("Please say the phone number.")
        phone_number = take_command() # Replace this with your voice input function to get the phone number

        speak("What message would you like to send?")
        message = take_command() # Replace with your voice input function to get the message

        send_sms(phone_number, message)
        speak("Your message has been sent.")
    elif "open stack overflow" in command:
        webbrowser.open("stackoverflow.com")
    
    else:
        speak("Please repeat the command again.")
    
    return False

# Main function to run the assistant
def main():
    speak("Welcome. I am your voice assistant.")
    while True:
        speak("How can I assist you?")
        command = take_command()
        command.lower()
        # Execute the task based on the command
        if execute_task(command):  # If the function returns True, exit the loop
            break


def send_sms(phone_number, message):
    response = requests.post('https://textbelt.com/text', {
        'phone': phone_number,
        'message': message,
        'key': 'textbelt',  # Use 'textbelt' for the free tier
    })

    result = response.json()
    if result['success']:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message: {result['error']}")

if __name__ == "__main__":
    main()
