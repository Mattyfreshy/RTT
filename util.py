import soundcard as sc
import soundfile as sf
import pyaudio
import base64
from time import sleep
import torch

from ASR.whisperASR import Wisp

OUTPUT_FILE_NAME = "output.wav"    # file name.
SAMPLE_RATE = 48000              # [Hz]. sampling rate.
RECORD_SEC = 5                  # [sec]. duration recording audio.

class Util:
    def __init__(self) -> None:
        self.FRAMES_PER_BUFFER = 3200
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.p = pyaudio.PyAudio()
    
    # Currently only works with Windows/linux due to MacOS not supporting loopback recording functionality.
    def print_all_speakers(self):
        print('All Speakers: \n', sc.all_speakers())
    
    def print_all_microphones(self):
        print('All Microphones: \n', sc.all_microphones())

    def print_default_speaker(self):
        print('Default Speaker: \n', sc.default_speaker())

    def print_default_microphone(self):
        print('Default Microphone: \n', sc.default_microphone())

    def print_all_devices(self):
        self.print_all_speakers()
        self.print_all_microphones()
        self.print_default_speaker()
        self.print_default_microphone()

    def record_audio(self, sample_rate=SAMPLE_RATE ,seconds=RECORD_SEC, output_file_name=OUTPUT_FILE_NAME):
        # record audio with loopback from default speaker.
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=sample_rate) as mic:
            # record audio with loopback from default speaker.
            data = mic.record(numframes=sample_rate*seconds)
            
            # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
            sf.write(file=output_file_name, data=data[:, 0], samplerate=sample_rate)

    def test(self):
        # starts recording
        stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER
        )

        while True:
            data = stream.read(self.FRAMES_PER_BUFFER)
            data = base64.b64encode(data).decode("utf-8")
            print(str(data))
            sleep(0.01)

    def test2(self, wisp: Wisp):
        # record audio with loopback from default speaker.
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
            # record audio with loopback from default speaker.
            data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)

            # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
            sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)
            
            # Get transcription from whisper
            wisp.transcribe(OUTPUT_FILE_NAME)

        pass

def main():
    wisp = Wisp()

    util = Util()
    # util.test2(wisp)
    print(torch.cuda.is_available())

if __name__ == "__main__":
    main()