import speech_recognition as sr
import pyttsx3
from Tools import ToolManager
import Agent

engine = pyttsx3.init()
recognizer = sr.Recognizer()
tool = ToolManager()

def wait_for_max():
    """Silently listens for 'max' before activating the agent."""
    with sr.Microphone() as source:
        print("Initializing...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=None)  # No console output
                user_input = recognizer.recognize_google(audio).lower()
                if "max" in user_input:
                    engine.say("Max is here! How can I help you today?")
                    engine.runAndWait()
                    return 
            except (sr.UnknownValueError, sr.RequestError):
                pass

def command_mode():
    """Handles commands until 'stop' is detected."""
    agent = Agent.get_agent()
    with sr.Microphone() as source:
        while True:
            try:
                audio = recognizer.listen(source, timeout=None)
                user_input = recognizer.recognize_google(audio)
                if "stop" in user_input.lower():
                    engine.say("Okay, you have a good day")
                    engine.runAndWait()
                    break
                res = agent.run(user_input)
                engine.say(res)
                engine.runAndWait()
            except (sr.UnknownValueError, sr.RequestError):
                pass  # Fail silently

def speak():
    """Main loop: Waits for 'max', then processes commands until 'stop'."""
    while True:
        wait_for_max()
        command_mode()