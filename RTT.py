from dotenv import load_dotenv
import time
import os

import openai
import pyttsx3
import speech_recognition as sr

# Load .env file
load_dotenv()

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize speech recognition engine for speaking
# engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except:
        print("Sorry, could not recognize audio")

def transcribe_whisper(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except:
        print("Sorry, could not recognize audio")
            
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=4000,
        n=1,
        stop=None
    )
    return response['choices'][0]['text']

# def speak_text(text):
#     engine.say(text)
#     engine.runAndWait()

def RTT(enable_response: bool = False):
    '''Records and transcribes audio to text'''
    try:
        # Record audio
        filename = 'voiceAssistant.wav'
        print("Recording...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            source.pause_threshold = 1
            audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())
            
        # Transcribe audio to text
        text = transcribe_audio_to_text(filename)
        if text:
            print(f"Transcription: {text}")
            
            # Generate response
            if enable_response:
                response = generate_response(text)
                print(f"Response: {response}")
            
            # read response using text-to-speech
            # if enable_text_to_speech:
                # speak_text(response)
                
    except Exception as e:
        print("[Voice Assistant] An error occurred: {}".format(e))
    
def translate():
    '''Translates audio to English using OpenAI's Whisper API'''
    try:
        # Record audio
        audio_file = 'translate.wav'
        print("Recording...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            source.pause_threshold = 1
            audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
            with open(audio_file, "wb") as f:
                f.write(audio.get_wav_data())
            
        # Transcribe audio to text
        transcript = openai.Audio.transcribe('whisper-1', audio_file)
        if transcript:
            print(f"Transcription: {transcript}")
            
            # Generate Translation
            response = openai.Audio.translate('whisper-1', transcript)
            print(f"Translation: {response}")
            
            # read response using text-to-speech
            # if enable_text_to_speech:
                # speak_text(response)
                
    except Exception as e:
        print("[Translate] An error occurred: {}".format(e))

def main():
    while True:
        # Voice Assistant Trigger
        trigger = "rice"
        # Print Trigger Options
        print(f"Say {trigger} to start voice assistant")
        print(f"Say translate to translate to English")
        with sr.Microphone() as source:
            # Set up the recognizer with the source
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            
            # Try converting audio to text
            try:
                transcription = recognizer.recognize_google(audio)
                # Match transcription to trigger
                if transcription.lower() == trigger:
                    RTT()
                elif transcription.lower() == "translate":
                    translate()
            except Exception as e:
                print("[Main] An error occurred: {}".format(e))
                
if __name__ == "__main__":
    main()