from dotenv import load_dotenv
import time
import os
from sys import platform

import openai
import speech_recognition as sr
import whisper
import pyaudio
import wave

from whisperASR import silent_whisper
import assemblyASR
from googleASR import GScribe

# Load .env file
load_dotenv()

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

class RTT:
    def __init__(self, model=None, microphone=None):
        self.model = model
        self.microphone = microphone if microphone else sr.Microphone()
        self.fp16 = True if platform == 'win32' else False

    def transcribe_audio_to_text(self, filename):
        """Transcribe audio to text. As of now, Google's Speech Recognition API is faster than Whisper"""
        if self.model is None:
            gscribe = GScribe()
            text = gscribe.transcribe_google(filename)
        else:
            wisp = silent_whisper(model=self.model)
            text = wisp.transcribe_whisper(filename)

        # Print transcription
        if text:
            print(f"Transcription: {text}")
            # print(text)

    def RTT_mic(self):
        """Records and transcribes mic audio to text"""
        try:
            # Record audio
            filename = 'RTT.wav'
            with self.microphone as source:
                recognizer = sr.Recognizer()
                recognizer.adjust_for_ambient_noise(source)
                source.energy_threshold = 300
                source.pause_threshold = 0
                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())
                
            # Transcribe audio to text. As of now, Google's Speech Recognition API is faster than Whisper
            self.transcribe_audio_to_text(filename)
                    
        except Exception as e:
            print("[RTT_mic] An error occurred: {}".format(e))

    def RTT_system(self):
        """Records and transcribes system audio to text"""
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
            self.transcribe_audio_to_text(self.model, WAVE_OUTPUT_FILENAME)

            pass
        except Exception as e:
            print("[RTT_system] An error occurred: {}".format(e))

def main():
    # Load Whisper Model
    # Whisper model sizes (tiny, base, small, medium, large)
    model = silent_whisper.load_model("base")
    
    # Debugging: Print all microphone names
    # print(sr.Microphone.list_microphone_names())
    microphone = sr.Microphone(device_index=1, sample_rate=16000)  # Microphone device index
    
    # Set model = None if you want to use Google's Speech Recognition API instead of Whisper
    rtt = RTT(model, microphone)

    # Start Recording
    print("\033[32mRecording...\033[37m(Ctrl+C to Quit)\033[0m")

    # Record and Transcribe Audio until Ctrl+C is pressed
    while True:    
        try:
            rtt.RTT_mic()
        except (KeyboardInterrupt, SystemExit): break

if __name__ == "__main__":
    main()