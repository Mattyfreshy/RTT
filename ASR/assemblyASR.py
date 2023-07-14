# pip install pyaudio requests websockets
import pyaudio
import websockets
import asyncio
import base64
import json
import os
from dotenv import load_dotenv

load_dotenv()

auth_key = os.getenv("ASSEMBLYAI_API_KEY")

class Ass:
    def __init__(self) -> None:
        self.FRAMES_PER_BUFFER = 3200
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.p = pyaudio.PyAudio()
        self.URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


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
                print("Sending messages ...")
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
                    while True:
                        try:
                            result_str = await _ws.recv()
                            if json.loads(result_str)['text'] != "":
                                print(json.loads(result_str)['text'])
                        except websockets.exceptions.ConnectionClosedError as e:
                            print(e)
                            assert e.code == 4008
                            break
                        except Exception as e:
                            assert False, "Not a websocket 4008 error"

                send_result, receive_result = await asyncio.gather(send(), receive())

        asyncio.run(send_receive())


def main():
    # To Run: python assemblyASR.py
    try:
        ass = Ass()
        ass.run()
    except (KeyboardInterrupt, SystemExit):
        print("Interrupted by user")
    except Exception as e:
        print("[Ass] An error occurred: {}".format(e))

if __name__ == "__main__":
    main()