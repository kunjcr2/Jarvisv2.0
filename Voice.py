import speech_recognition as sr
import pyttsx3
from Tools import ToolManager
import Agent

engine = pyttsx3.init()
recognizer = sr.Recognizer()
tool = ToolManager()

# for 
def for_max():
    while True:
        print("Listening...")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                user_input = recognizer.recognize_google(audio).lower()
                if "max" in user_input:
                    print("Max is here! How can I help you today?")
                    engine.say("Max is here! How can I help you today?")
                    engine.runAndWait()
                    return
                else:
                    continue
            except sr.UnknownValueError:
                print("Sorry, I did not understand.")
            except sr.RequestError:
                print("Service is down.")

# for listening and speaking
def for_agent():
    agent = Agent.get_agent()
    while True:
        tool.__init__()
        print("Listening for command...")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                user_input = recognizer.recognize_google(audio)
                if "stop" in user_input.lower():
                    engine.say("Okay, you have a good day")
                    engine.runAndWait()
                    break
                else:
                    res = agent.run(user_input)
                    engine.say(res)
                    engine.runAndWait()
            except sr.UnknownValueError:
                print("Sorry, I did not understand.")
            except sr.RequestError:
                print("Service is down.")

def speak():
    # for_max()
    for_agent()
