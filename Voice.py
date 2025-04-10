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
                audio = recognizer.listen(source, timeout=None)
                user_input = recognizer.recognize_google(audio).lower()
                if "max" in user_input:
                    engine.say("Max is here! How can I help you today?")
                    engine.runAndWait()
                    return 
            except (sr.UnknownValueError, sr.RequestError):
                pass

def command_mode():
    """Handles commands until 'stop' is detected. Only processes commands starting with 'max'."""
    agent = Agent.get_agent()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        while True:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=None)
                user_input = recognizer.recognize_google(audio)
                print("Heard:", user_input)
                
                user_input_lower = user_input.lower()

                if "stop" in user_input_lower:
                    engine.say("Okay, you have a good day")
                    engine.runAndWait()
                    break
                
                if user_input_lower.strip().startswith("max"):

                    max_index = user_input_lower.find("max")
                    actual_command = user_input[max_index + 3:].strip()
                    
                    if actual_command:
                        print("Processing command:", actual_command)
                        res = agent.run(actual_command)
                        engine.say(res)
                        engine.runAndWait()
                    else:
                        engine.say("I didn't hear a command after max")
                        engine.runAndWait()
            except Exception as e:
                pass

def speak():
    """Main loop: Waits for 'max', then processes commands until 'stop'."""
    # wait_for_max()
    command_mode()
