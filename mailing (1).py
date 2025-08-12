import smtplib
import speech_recognition as sr
import pyttsx3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Email credentials (use environment variables in production for security)
EMAIL_ADDRESS = "zendesk2024@gmail.com"
EMAIL_PASSWORD = "anpo zmbc dgbh rolp"

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands using Google Web Speech API
def take_command():
    with sr.Microphone() as source:
        # Adjust for ambient noise and set a higher energy threshold
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.energy_threshold = 300  # Increase for noisy environments
        print("Listening...")
        try:
            # Set a timeout for listening
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            # Use Google Web Speech API for recognition
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out, please try again.")
            speak("Listening timed out, please try again.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand. Could you repeat?")
            speak("Sorry, I couldn't understand. Could you repeat?")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            speak("Could not request results from Google Speech Recognition service.")
        return None

# Function to send an email
def send_email(recipient, subject, message):
    try:
        # Create a MIME object for the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = subject

        # Attach the body of the email
        msg.attach(MIMEText(message, 'plain'))

        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to secure
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Send the email
        server.send_message(msg)
        server.quit()

        speak("Email has been sent successfully.")
        print("Email sent!")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")
        print(f"An error occurred: {e}")

# Main function to handle sending email through voice command
# Main function to handle sending email through voice command
# Function to replace spoken "dot" with a period in the email ID
def format_email_id(recipient_id):
    if recipient_id:
        # Replace spoken equivalents with actual symbols
        recipient_id = recipient_id.replace(" dot ", ".")
        recipient_id = recipient_id.replace(" underscore ", "_")
        recipient_id = recipient_id.replace(" dash ", "-")
        recipient_id = recipient_id.replace(" hyphen ", "-")
        recipient_id = recipient_id.replace(" plus ", "+")
        recipient_id = recipient_id.replace(" at the rate ", "@")
        recipient_id = recipient_id.replace(" at ", "@")
        
        # Remove any extra spaces that may have been spoken
        recipient_id = recipient_id.replace(" ", "")
    return recipient_id


# Main function to handle sending email through voice command
def send_email_command():
    speak("  Please say the email ID before '@gmail.com'.")
    recipient_id = take_command()

    if recipient_id:
        # Format the recipient ID to replace "dot" with "."
        recipient_id = format_email_id(recipient_id)
        # Automatically append "@gmail.com"
        recipient = f"{recipient_id}@gmail.com"

        speak("What is the subject of the email?")
        subject = take_command()

        speak("What message do you want to send?")
        message = take_command()

        # Send the email if all details are provided
        if subject and message:
            send_email(recipient, subject, message)
        else:
            speak("Sorry, some information was missing. Please try again.")
            print("Incomplete email details.")
    else:
        speak("Sorry, I didn't catch the email ID. Please try again.")



# Call the main function
if __name__ == "__main__":
    send_email_command()
