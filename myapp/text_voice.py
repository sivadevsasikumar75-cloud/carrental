
import pyttsx3

def speak(message):
    engine = pyttsx3.init()
    engine.setProperty("volume", 1.0)
    engine.say(message)
    engine.runAndWait()
    engine.stop()
    del engine

speak("Hello, this is a voice test.")
speak("The current time is eleven thirty AM.")
speak("Goodbye!")

print("Test completed")
