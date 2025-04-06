import wikipedia
import pywhatkit as kit
import requests
import webbrowser
from langchain.agents import Tool
from youtubesearchpython import VideosSearch

# Email support
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from langchain_openai import ChatOpenAI
import ast

# Google Calendar reminder
import urllib.parse
from datetime import datetime, timedelta

# Environment variables
import os
from dotenv import load_dotenv

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
    res = kit.search(query)
    return res
def get_llm():
    '''
    LLM
    '''
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    try:
        llm = ChatOpenAI(
            api_key=api_key,
            model="gpt-3.5-turbo"
        )
        return llm
    except Exception as e:
        print(f"Error initializing ChatOpenAI: {str(e)}")
        raise
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

    EMAIL = os.getenv('EMAIL_ADDRESS')
    PASSWORD = os.getenv('EMAIL_PASSWORD')

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
        # Parse the query string
        parts = query.split(",") + [""] * (5 - len(query.split(",")))
        title = parts[0].strip()
        
        # Get date (default: today)
        date_str = parts[1].strip() or datetime.now().strftime("%Y-%m-%d")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Get time (default: current time)
        time_str = parts[2].strip() or datetime.now().strftime("%H:%M")
        hour, minute = map(int, time_str.split(":"))
        
        # Create datetime object
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

####################################################################################################################

###############################################---Tools---###############################################################
# For getting the tools and using google ONCE
class ToolManager:
    def __init__(self):
        self.google_used = False
        self.web_used = False

    # These are the tools here
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
            description="Use ONLY for sending professional emails to a specific email address and return stricly in dictionary format 'subject', 'body' and you can use \\n.",
            func=send_email
        )
        reminder_tool = Tool(
            name="Reminder",
            description="Create a reminder in Google Calendar using a simple format: 'title, date (YYYY-MM-DD), time (HH:MM), description, duration (minutes)'. Only title is required.",
            func=add_google_calendar_reminder
        )

        llm_tool = Tool(
            name="OpenAI",
            description="Answers questions when Wikipedia lacks information. Use sparingly.",
            func=get_llm().invoke
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
        ]

    # This is the function to use google
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