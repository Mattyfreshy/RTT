from dotenv import load_dotenv
import time
import os

import openai
import speech_recognition as sr

# Load .env file
load_dotenv()

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio_to_text(filename):
    '''Transcribes audio to text using Google's Speech Recognition API'''
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except:
        print("Sorry, could not recognize audio")

def transcribe_whisper(filename):
    '''Transcribes audio to text using OpenAI's Whisper API'''
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except:
        print("Sorry, could not recognize audio")
            
def generate_response(prompt):
    '''Generates a response to a prompt using OpenAI's Davinci API'''
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=4000,
        n=1,
        stop=None
    )
    return response['choices'][0]['text']

def RTT():
    '''Records and transcribes audio to text'''
    try:
        # Record audio
        filename = 'RTT.wav'
        # print("Recording...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            source.pause_threshold = 1
            audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())
            
        # Transcribe audio to text
        text = transcribe_audio_to_text(filename)
        if text:
            # print(f"Transcription: {text}")
            print(text)
                
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
                
    except Exception as e:
        print("[Translate] An error occurred: {}".format(e))

def main():
    print("Recording...")
    while True:    
        # Live Transcription
        try:
            RTT()
        except Exception as e:
            print("[Main] An error occurred: {}".format(e))
                
if __name__ == "__main__":
    main()