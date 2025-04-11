import speech_recognition as sr
import pyttsx3
from src.Tools import ToolManager
import src.Agent as Agent

from src.Context import Context

engine = pyttsx3.init()
recognizer = sr.Recognizer()
recognizer.pause_threshold = 2
tool = ToolManager()
ctx = Context()

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
        recognizer.adjust_for_ambient_noise(source, duration=1)
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
                    command_with_context = ""
                    
                    if actual_command.strip().startswith(("and", "but", "what about", "how about")):
                        command_with_context = f"last command was {ctx.get_context()}, answer ONLY {actual_command}"
                        actual_command = ""
                    
                    command = command_with_context or actual_command
                    if command:
                        print("Processing command:", command)
                        res = agent.run(command)
                        ctx.add_context(command)
                        engine.say(res)
                        engine.runAndWait()
                    else:
                        engine.say("I didn't hear a command after max")
                        engine.runAndWait()
                else:
                    print("Did not find max") ###
            except Exception as e:
                pass

def speak():
    """Main loop: Waits for 'max', then processes commands until 'stop'."""
    # wait_for_max()
    command_mode()
