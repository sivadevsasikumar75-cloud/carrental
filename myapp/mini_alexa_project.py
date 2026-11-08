
import pyttsx3
import datetime
import webbrowser


# Function to speak
def speak(message):
    engine = pyttsx3.init()
    engine.setProperty("volume", 1.0)
    engine.say(message)
    engine.runAndWait()
    engine.stop()
    del engine


# Main program
while True:
    command = input("You: ").lower().strip()

    if "hello" in command or command == "hi":
        message = "Hello! How can I help you?"

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        message = "The current time is " + current_time

    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        message = "Today's date is " + current_date

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        message = "Opening Google"

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        message = "Opening YouTube"

    elif command == "exit" or command == "stop":
        message = "Goodbye!"

    else:
        message = "Sorry, I don't understand that command."

    print("Alexa:", message)
    speak(message)

    if command == "exit" or command == "stop":
        break
