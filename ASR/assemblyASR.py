# pip install pyaudio requests websockets
import pyaudio
import websockets
import asyncio
import base64
import json
import os
import string
from dotenv import load_dotenv

load_dotenv()

auth_key = os.getenv("ASSEMBLYAI_API_KEY")

# ANSI escape codes for erasing the current line
ERASE_LINE = '\x1b[2K' 


class Ass:
    def __init__(self, inline=True, frames_per_buffer=3200, format=pyaudio.paInt16, channels=1, rate=16000, p=pyaudio.PyAudio()) -> None:
        """
        If inline = true, print the result on the same line.
        """
        self.FRAMES_PER_BUFFER = frames_per_buffer
        self.FORMAT = format
        self.CHANNELS = channels
        self.RATE = rate
        self.p = p
        self.URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=" + str(rate)
        self.inline = inline

    def run(self):
        # starts recording
        stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER
        )

        # the AssemblyAI endpoint we're going to hit
        URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

        async def send_receive():
            print(f'Connecting websocket to url ${URL}')
            async with websockets.connect(
                URL,
                extra_headers=(("Authorization", auth_key),),
                ping_interval=5,
                ping_timeout=20
            ) as _ws:
                await asyncio.sleep(0.1)
                print("Receiving SessionBegins ...")
                session_begins = await _ws.recv()
                print(session_begins)
                print("Sending/Transcribing messages ...")
                async def send():
                    while True:
                        try:
                            data = stream.read(self.FRAMES_PER_BUFFER)
                            data = base64.b64encode(data).decode("utf-8")
                            json_data = json.dumps({"audio_data":str(data)})
                            await _ws.send(json_data)
                        except websockets.exceptions.ConnectionClosedError as e:
                            print(e)
                            assert e.code == 4008
                            break
                        except Exception as e:
                            assert False, "Not a websocket 4008 error"
                        await asyncio.sleep(0.01)

                async def receive():
                    # Conditional to prevent overwriting the previous line in certain cases
                    prev_line = None
                    while True:
                        try:
                            # Receive the result and load it into a json object
                            result_str = await _ws.recv()
                            json_result = str(json.loads(result_str)['text'])

                            # If result is not empty, print the result
                            if json_result != "":
                                ### Make new line if sentence finished else edit inline
                                # Clean the json result and the previous line of punctuation
                                json_clean = json_result.translate(str.maketrans('', '', string.punctuation))
                                prev_clean = prev_line.translate(str.maketrans('', '', string.punctuation)) if prev_line else json_clean
                                # print("json_clean: ", json_clean)
                                # print("prev_clean: ", prev_clean)

                                # If inline is true, print the result on the same line
                                if self.inline:
                                    if prev_line and prev_clean.lower() in json_clean.lower():
                                        print(ERASE_LINE + json_result, end="\r")
                                    else:
                                        print()
                                else:
                                    print(json_result)
                                prev_line = json_result

                        except websockets.exceptions.ConnectionClosedError as e:
                            print(e)
                            assert e.code == 4008
                            break
                        except Exception as e:
                            print(e)
                            assert False, "Not a websocket 4008 error"

                send_result, receive_result = await asyncio.gather(send(), receive())

        asyncio.run(send_receive())


def main():
    # To Run: python assemblyASR.py
    try:
        ass = Ass(inline=True)
        ass.run()
    except (KeyboardInterrupt, SystemExit):
        print("Interrupted by user")
    except Exception as e:
        print("[Ass] An error occurred: {}".format(e))

if __name__ == "__main__":
    main()