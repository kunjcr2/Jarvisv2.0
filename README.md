# Jarvis v2.0

> Voice activated assistant using AI Agent and tools to do various tasks

## Overview

Jarvis v2.0 is an intelligent voice assistant that uses speech recognition and text-to-speech capabilities to interact with users. It can understand voice commands and respond with appropriate actions or information.

## Features

- Voice command recognition using Google Speech Recognition
- Text-to-speech responses using pyttsx3
- Modular tool system for executing various tasks
- Agent-based architecture for processing commands
- Wake word detection ("Max")

## Updated Features

- **Memory Integration**: The agent now retains the last command using a memory buffer for improved context handling.
- **Enhanced Context Management**: The `Context.py` module has been updated to provide better context handling for commands.
- **Improved Tool System**: The `Tools.py` module now supports a wider range of tools with better extensibility.

## Project Structure

- `driver.py`: Main entry point of the application
- `src/`
  - `Agent.py`: Manages the AI agent that processes commands, now updated to include better modularity and error handling.
  - `Context.py`: Manages context for commands, updated for better context resolution.
  - `llm.py`: Handles interactions with the language model, updated for improved API integration and now includes memory integration for retaining the last command.
  - `test.py`: Contains test cases for validating the functionality of various modules.
  - `Tools.py`: Contains various tools and utilities for task execution, updated for better tool management.
  - `Voice.py`: Handles voice recognition and text-to-speech functionality, updated for enhanced user interaction.
  - `__pycache__/`: Stores compiled Python files for faster execution.

## Prerequisites

- Python 3.x
- Required Python packages:
  - speech_recognition
  - pyttsx3
  - langchain
  - python-dotenv
  - (other dependencies will be listed in requirements.txt)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Jarvisv2.0.git
cd Jarvisv2.0
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables in the `.env` file:

```bash
EMAIL="your_email"                        # for email where you want geenrated emails to go
PASSWORD="your_temporary_google_password" # Contact me for this, it is called "passkey"
OPENAI_API_KEY="your_openai_api_key"      # Contact me for help
```

## Usage

1. Run the application:

```bash
python driver.py
```

2. Wait for the wake word "Max" or start speaking commands directly
3. Speak your command clearly
4. Say "stop" to end the session

## Recent Updates

- Added `src.` prefix to all imports for better module resolution.
- Improved error handling and modularity across all files in the `src` folder.
- Enhanced the voice recognition and command processing logic in `Voice.py`.
- Updated `Agent.py` to include a more robust agent initialization process.
- Refactored `Tools.py` for better tool management and extensibility.

## Tools Available

- **Wikipedia Tool**: Fetches a brief summary from Wikipedia for a given query.
- **Google Search Tool**: Performs a Google search for real-time or media-related queries. Can only be used once per query.
- **YouTube Tool**: Streams media on YouTube and returns the title of the searched content.
- **Google Maps Tool**: Opens Google Maps for directions or location searches.
- **Web Search Tool**: Opens specific websites and returns the name of the site.
- **Weather Tool**: Provides the current weather for a specified location.
- **Email Tool**: Sends professional emails with a subject and body. Requires dictionary input with 'subject' and 'body'.
- **Reminder Tool**: Creates a Google Calendar reminder using a simple format: 'title, date (YYYY-MM-DD), time (HH:MM), description, duration (minutes)'. Only the title is required.
- **General LLM Fallback**: If the agent fails to find a solution using the available tools, it falls back to a default Language Learning Model (LLM) to process the query and provide a response.
- **Camera Tool**: Captures images or video using the system's camera.
- **File Writing Tool**: Creates or appends content to files in the workspace, with automatic file creation if it doesn't exist.
- **Screenshot Tool**: A new tool has been added to take screenshots using the `pyautogui` library. This tool saves screenshots with a timestamped filename in the `screenshots` directory. To use this tool, ensure the `pyautogui` library is installed (already included in `requirements.txt`).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Google Speech Recognition API
- pyttsx3 library
- All contributors and maintainers
