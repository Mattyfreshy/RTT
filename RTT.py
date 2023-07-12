from dotenv import load_dotenv
import time
import os
from sys import platform

import openai
import speech_recognition as sr
import whisper
import pyaudio
import wave

# Load .env file
load_dotenv()

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_google(filename):
    '''Transcribes audio to text using Google's Speech Recognition API'''
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except:
        print("...")

def transcribe_whisper(model: whisper, filename):
    '''Transcribes audio to text using Whisper'''
    try:
        if platform == 'win32':
            # Windows
            fp16=True
        else:
            # Mac OS/Linux
            fp16=False
        
        result = model.transcribe(filename, fp16=fp16, language='english', condition_on_previous_text=False)
        return result["text"]
    except Exception as e:
        print("[Whisper] An error occurred: {}".format(e))
        # print("...")
            

def transcribe_audio_to_text(model, filename):
    # Transcribe audio to text. As of now, Google's Speech Recognition API is faster than Whisper
    if model is None:
        text = transcribe_google(filename)
    else:
        text = transcribe_whisper(model, filename)

    # Print transcription
    if text:
        print(f"Transcription: {text}")
        # print(text)

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

def RTT_mic(model: whisper, microphone: sr.Microphone):
    '''Records and transcribes mic audio to text'''
    try:
        # Record audio
        filename = 'RTT.wav'
        with microphone as source:
            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(source)
            source.energy_threshold = 300
            source.pause_threshold = 0
            audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())
            
        # Transcribe audio to text. As of now, Google's Speech Recognition API is faster than Whisper
        transcribe_audio_to_text(model, filename)
                
    except Exception as e:
        print("[RTT_mic] An error occurred: {}".format(e))

def RTT_system(model: whisper):
    '''Records and transcribes system audio to text'''
    try:
        # Record audio
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "output.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))


        # Transcribe audio to text. As of now, Google's Speech Recognition API is faster than Whisper
        transcribe_audio_to_text(model, WAVE_OUTPUT_FILENAME)

        pass
    except Exception as e:
        print("[RTT_system] An error occurred: {}".format(e))
    
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
    model = whisper.load_model('base')         # Whisper model size (tiny, base, small, medium, large)
    print("\033[32mRecording...\033[37m(Ctrl+C to Quit)\033[0m")
    
    # Debugging: Print all microphone names
    # print(sr.Microphone.list_microphone_names())
    microphone = sr.Microphone(device_index=1, sample_rate=16000)  # Microphone device index
    
    while True:    
        # Live Transcription w/ Whisper
        try:
            # Set model = None if you want to use Google's Speech Recognition API
            RTT_mic(model, microphone)
        except (KeyboardInterrupt, SystemExit): break

if __name__ == "__main__":
    main()