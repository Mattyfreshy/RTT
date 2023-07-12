# Real Time Transcription

Goal of this project is to create a real time transcription tool that can be used to transcribe audio from microphone and output to text.

## Features
- Transcribe audio from microphone and output to text in terminal.

## Requirements
- Python 3.6 or higher
- All requirements in requirements.txt  

### Note
If could not build wheels for pyaudio, 
On Mac
```
brew install portaudio
```

On Linux
```
sudo apt-get install portaudio19-dev
```
Then try again

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Navigate into the project directory:

   ```bash
   cd RTTVoiceAssistant
   ```

4. Create a new virtual environment:

   ```bash
   python -m venv venv
   . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file:

   ```bash
   cp .env.example .env
   ```

7. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

8. Run the app using python or python3 depending on your system:

   ```bash
   python Voice_GPT3.py
   ```
# RTT
