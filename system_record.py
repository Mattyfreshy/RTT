import soundcard as sc
import soundfile as sf

OUTPUT_FILE_NAME = "output.wav"    # file name.
SAMPLE_RATE = 48000              # [Hz]. sampling rate.
RECORD_SEC = 5                  # [sec]. duration recording audio.
GAIN_FACTOR = 10.0               # gain factor for amplifying audio. (1.0 = no amplification)


# Currently only works with Windows/linux due to MacOS not supporting loopback recording functionality.
print('All Speakers: \n', sc.all_speakers())
print('All Microphones: \n', sc.all_microphones())
print('Default Speaker: \n', sc.default_speaker())

# record audio with loopback from default speaker.
with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
    # record audio with loopback from default speaker.
    data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)

    # Amplify the audio
    data = data * GAIN_FACTOR
    
    # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
    sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)