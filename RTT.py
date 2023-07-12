from dotenv import load_dotenv
import time
import os

import openai
import speech_recognition as sr
import whisper

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
        print("...")

def transcribe_whisper(model, filename):
    '''Transcribes audio to text using Whisper'''
    try:
        result = model.transcribe(filename, fp16=False, language='english')
        return result["text"]
    except:
        print("...")
            
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

def RTT(model, microphone):
    '''Records and transcribes audio to text'''
    try:
        # Record audio
        filename = 'RTT.wav'
        # print("Recording...")
        with microphone as source:
            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(source)
            source.pause_threshold = 0
            audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())
            
        # Transcribe audio to text. As of now, Google's Speech Recognition API is faster than Whisper
        text = transcribe_audio_to_text(filename)
        # text = transcribe_whisper(model, filename)
        if text:
            print(f"Transcription: {text}")
            # print(text)
                
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

def main(loop=False):
    print("\033[32mLoading Whisper Model...\033[37m")
    model = whisper.load_model('small')         # Whisper model size (tiny, base, small, medium, large)
    print("\033[32mRecording...\033[37m(Ctrl+C to Quit)\033[0m")
    # Debugging: Print all microphone names
    # print(sr.Microphone.list_microphone_names())
    microphone = sr.Microphone(device_index=1)  # Microphone device index
    while True:    
        # Live Transcription w/ Whisper
        try:
            RTT(model, microphone)
        except (KeyboardInterrupt, SystemExit): break

if __name__ == "__main__":
    main()