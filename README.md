# Jarvis v2.0

A voice-controlled AI assistant that can perform various tasks through natural language commands.

## Overview

Jarvis v2.0 is an intelligent voice assistant that uses speech recognition and text-to-speech capabilities to interact with users. It can understand voice commands and respond with appropriate actions or information.

## Features

- Voice command recognition using Google Speech Recognition
- Text-to-speech responses using pyttsx3
- Modular tool system for executing various tasks
- Agent-based architecture for processing commands
- Wake word detection ("Max")

## Project Structure

- `driver.py`: Main entry point of the application
- `Voice.py`: Handles voice recognition and text-to-speech functionality
- `Tools.py`: Contains various tools and utilities for task execution
- `Agent.py`: Manages the AI agent that processes commands
- `.env`: Configuration file for environment variables

## Prerequisites

- Python 3.x
- Required Python packages:
  - speech_recognition
  - pyttsx3
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

3. Set up your environment variables in the `.env` file

## Usage

1. Run the application:

```bash
python driver.py
```

2. Wait for the wake word "Max" or start speaking commands directly
3. Speak your command clearly
4. Say "stop" to end the session

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Speech Recognition API
- pyttsx3 library
- All contributors and maintainers
