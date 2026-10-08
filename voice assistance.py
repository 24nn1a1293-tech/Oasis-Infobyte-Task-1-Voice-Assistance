import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
from urllib.parse import quote

# Initialize
recognizer = sr.Recognizer()
engine = pyttsx3.init()

engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)


# Text to Speech
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# Voice Input
def listen():
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

            print("Recognizing...")
            command = recognizer.recognize_google(audio)

            print("You:", command)

            return command.lower()

        except sr.UnknownValueError:
            speak("Sorry, I could not understand. Please try again.")
            return ""

        except sr.WaitTimeoutError:
            speak("I did not hear anything.")
            return ""

        except sr.RequestError:
            speak("Speech recognition service is not available.")
            return ""


# Tell Time
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak("The current time is " + current_time)


# Tell Date
def tell_date():
    current_date = datetime.datetime.now().strftime("%d %B %Y")
    speak("Today's date is " + current_date)


# Open Website
def open_website(command):

    # Remove "open" from the command
    website = command.replace("open", "", 1).strip()

    if website == "":
        speak("Please tell me what you want to open.")
        return

    # Some common websites
    websites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "gmail": "https://mail.google.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "whatsapp": "https://web.whatsapp.com",
        "spotify": "https://open.spotify.com",
        "github": "https://github.com",
        "linkedin": "https://www.linkedin.com",
        "chatgpt": "https://chatgpt.com",
        "wikipedia": "https://www.wikipedia.org"
    }

    # If it is a known website
    if website in websites:
        speak("Opening " + website)
        webbrowser.open(websites[website])

    else:
        # Try to open it as a website
        if "." in website:
            url = "https://" + website
            speak("Opening " + website)
            webbrowser.open(url)

        else:
            # If not a known website, search Google
            speak("I could not find the website. Searching for " + website)

            search_url = "https://www.google.com/search?q=" + quote(website)
            webbrowser.open(search_url)


# Google Search
def web_search(command):

    query = command

    query = query.replace("search for", "")
    query = query.replace("search", "")
    query = query.replace("google", "")
    query = query.strip()

    if query:
        speak("Searching for " + query)

        url = "https://www.google.com/search?q=" + quote(query)

        webbrowser.open(url)

    else:
        speak("Please tell me what you want to search for.")


# Process Commands
def process_command(command):

    if command == "":
        return True

    # Greeting
    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")

    # Open anything
    elif command.startswith("open "):
        open_website(command)

    # Time
    elif "time" in command:
        tell_time()

    # Date
    elif "date" in command or "today" in command:
        tell_date()

    # Search
    elif "search" in command or "google" in command:
        web_search(command)

    # Exit
    elif "exit" in command or "stop" in command or "goodbye" in command:
        speak("Goodbye! Have a nice day.")
        return False

    # Unknown command
    else:
        speak("Sorry, I don't know that command.")

    return True


# Main Program
def main():

    speak("Hello! I am your voice assistant.")

    while True:

        command = listen()

        if not process_command(command):
            break


# Start program
if __name__ == "__main__":
    main()