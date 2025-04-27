import wikipedia
import pywhatkit as kit
import requests
import webbrowser
from langchain.agents import Tool
from youtubesearchpython import VideosSearch
import googlesearch as search

# Email support
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from langchain_openai import ChatOpenAI
import ast

# Google Calendar reminder
import urllib.parse
from datetime import datetime, timedelta

# opencv
import cv2
import random

# Environment variables
import os
from dotenv import load_dotenv

# pyautogui for screenshots
import pyautogui

# Load environment variables
load_dotenv()

###############################################---TOOLS---#########################################################
def get_wikipedia_summary(query):
    '''
    Used to get a summary from Wikipedia.
    '''
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception as e:
        print(e)
def google_search(query):
    '''
    Used for google searching
    '''
    for i in range(1):
        for i in search(query, num_results=1):
            link = i
            break

    webbrowser.open(link)
    return "Opened it on the browser. JOB DONE."

def get_yt(query):
    search = VideosSearch(query, limit = 1)
    results = search.result()

    if results['result']:
        id = results['result'][0]['id']

    webbrowser.open(f"https://www.youtube.com/watch?v={id}")

    return "Opened it on the browser. JOB DONE."
def get_map(query):
    URL = f"https://www.google.co.in/maps/search/{query.replace(' ', '+')}/"
    webbrowser.open(URL)

    return "Opened it on the browser. JOB DONE."
def get_web(query):
    query = query.replace(" ", "")

    URL = f"https://www.{query.lower()}.com"
    webbrowser.open(URL)
def get_weather(where):
    return requests.get(f"https://wttr.in/{where}?format=%C+%t").text
def send_email(dict):

    dict = ast.literal_eval(dict)

    subject = dict["subject"]
    body = dict["body"]

    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL, EMAIL, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
def add_google_calendar_reminder(query):
    """
    Opens Google Calendar with prefilled reminder details.
    No API keys required - just opens a URL in the browser.
    
    Parameters:
        query (str): Format: "title, date, time, description, duration"
                     Only title is required, others are optional
                     date: YYYY-MM-DD (default: today)
                     time: HH:MM (default: current time)
                     duration: minutes (default: 60)
    
    Returns:
        dict: Result information
    """
    try:
        parts = query.split(",") + [""] * (5 - len(query.split(",")))
        title = parts[0].strip()
        
        date_str = parts[1].strip() or datetime.now().strftime("%Y-%m-%d")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        
        time_str = parts[2].strip() or datetime.now().strftime("%H:%M")
        hour, minute = map(int, time_str.split(":"))
        
        event_time = datetime(
            date_obj.year, date_obj.month, date_obj.day, hour, minute
        )
        
        # Get description and duration
        description = parts[3].strip()
        duration = int(parts[4]) if parts[4].strip() else 60

        # Format times for Google Calendar
        start_time = event_time.strftime("%Y%m%dT%H%M%S")
        end_time = (event_time + timedelta(minutes=duration)).strftime("%Y%m%dT%H%M%S")
        
        # Create and open Google Calendar URL
        url = "https://calendar.google.com/calendar/render?" + urllib.parse.urlencode({
            "action": "TEMPLATE",
            "text": title,
            "dates": f"{start_time}/{end_time}",
            "details": description,
            "sf": "true",
            "output": "xml"
        })
        
        webbrowser.open(url)
        
        return {
            "success": True,
            "message": "Google Calendar opened with your reminder",
            "details": {
                "title": title,
                "date": date_str,
                "time": time_str,
                "duration": duration
            }
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}
def get_pic(bool):
    if bool:
        img_dir = os.path.join(".", "image")
    
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)

        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            return "Error: Could not open camera."

        ret, frame = camera.read()
        if not ret:
            camera.release()
            return "Error: Could not read frame."
        
        while True:
            img_name = f'img{random.randint(1,1000)}.jpg'
            img_path = os.path.join(img_dir, img_name)
            if not os.path.exists(img_path):
                break

        cv2.imwrite(img_path, frame)
        camera.release()

        return "Taken a picture successfully."
    else:
        return "Camera is not opened."
def write_to_file(file):
    """
    Writes content to a file. If the file doesn't exist, it will create it. 
    If it exists, it will append the content.
    """
    try:
        file = ast.literal_eval(file)
        filename, content = file[0], file[1]
        filename = filename.replace(" ", "_")

        filename = f'./files/{filename}'
        if not os.path.exists(filename):

            with open(filename, 'w') as f:
                f.write(content + "\n")
                return f"File '{filename}' did not exist, so it was created and content was written."
        else:

            with open(filename, 'a') as f:
                f.write(content + "\n")
                return f"Content was appended to the file '{filename}'."
    except Exception as e:
        return f"It didnt work."
    
def take_screenshot(save_directory="images"):
    """
    Takes a screenshot and saves it to the specified directory with a timestamped filename.

    Args:
        save_directory (str): The directory where the screenshot will be saved. Defaults to 'screenshots'.

    Returns:
        str: The file path of the saved screenshot.
    """
    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(save_directory, f"screenshot_{timestamp}.png")

    # Take the screenshot and save it
    screenshot = pyautogui.screenshot()
    screenshot.save(file_path)

    return file_path

####################################################################################################################

###############################################---Google Tool---###############################################################
# For getting the tools and using google ONCE
class ToolManager:
    def __init__(self):
        self.google_used = False
        self.web_used = False
    def get_tools(self):
        wiki_tool = Tool(
            name="Wikipedia", 
            description="Fetches information from Wikipedia. USE ONLY ONCE", 
            func=get_wikipedia_summary
        )
        google_tool = Tool(
            name="Google",
            description="Use ONLY ONCE per query for live match scores, opening specific sites, finding images, or other real-time/media-related searches.",
            func=self.use_google
        )
        yt_tool = Tool(
            name="YouTube",
            description="Use ONLY for streaming media on YouTube and return the title you searched ONLY",
            func=get_yt
        )
        map_tool = Tool(
            name="Google Maps",
            description="Use ONLY for getting directions or searching on Google Maps.",
            func=get_map
        )
        web_tool = Tool(
            name="Web Search",
            description="Use ONLY ONCE for opening specific sites and return the name of it ONLY.",
            func=get_web
        )
        weather_tool = Tool(
            name="Weather",
            description="Use ONLY for getting the weather of a specific location.",
            func=get_weather
        )
        email_tool = Tool(
            name="Email",
            description="Use ONLY for sending professional emails of MORE THAN ONE LINE to a specific email address and return stricly in dictionary format 'subject', 'body' and you can use \\n.",
            func=send_email
        )
        reminder_tool = Tool(
            name="Reminder",
            description="Create a reminder in Google Calendar using a simple format: 'title, date (YYYY-MM-DD), time (HH:MM), description, duration (minutes)'. Only title is required.",
            func=add_google_calendar_reminder
        )
        camera_tool = Tool(
            name="Camera",
            description="Use ONLY for taking a picture, return True or False.",
            func=get_pic
        )
        file_tool = Tool(
            name="write_file",
            description="Use ONLY to write to a file or 'save it', Return [filename, content]",
            func=write_to_file
        )
        screenshot_tool = Tool(
            name="Screenshot",
            description="Use ONLY for taking a screenshot and saving it with a timestamped filename.",
            func=take_screenshot
        )
        
        return [
            wiki_tool, 
            google_tool, 
            yt_tool,    
            map_tool,
            web_tool,
            weather_tool,
            email_tool,
            reminder_tool,
            camera_tool,
            file_tool,
            screenshot_tool
        ]
    def use_google(self, query):
        if self.google_used:
            return "Google search already used in this query."
        self.google_used = True
        return google_search(query)

    def use_web(self, query):
        if self.web_used:
            return "Google search already used in this query."
        self.web_used = True
        return get_web(query)
####################################################################################################################
