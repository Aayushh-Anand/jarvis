import json
import os
import time

import pyaudiowpatch as pyaudio
from vosk import Model, KaldiRecognizer


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "vosk-model-small-en-us-0.15"
)

MICROPHONE_INDEX = 1

SAMPLE_RATE = 16000
CHANNELS = 1
FORMAT = pyaudio.paInt16
CHUNK_SIZE = 4000


class OfflineSpeechToText:
    def __init__(
        self,
        model_path: str = MODEL_PATH,
        microphone_index: int = MICROPHONE_INDEX
    ):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                "Vosk model not found.\n"
                f"Expected location:\n{model_path}"
            )

        print("Loading offline Vosk model...")

        self.model = Model(model_path)

        self.microphone_index = microphone_index

        self.audio = pyaudio.PyAudio()

        print("Offline speech recognition ready.")

    def listen(
        self,
        timeout: int = 8
    ) -> str | None:

        recognizer = KaldiRecognizer(
            self.model,
            SAMPLE_RATE
        )

        recognizer.SetWords(False)

        try:
            stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                input=True,
                input_device_index=self.microphone_index,
                frames_per_buffer=CHUNK_SIZE
            )

        except Exception as e:
            print(
                "Microphone initialization failed:"
            )
            print(
                f"{type(e).__name__}: {e}"
            )
            return None

        print()
        print("🎤 Listening...")

        stream.start_stream()

        start_time = time.time()

        last_text = ""

        try:

            while (
                time.time() - start_time
                < timeout
            ):

                data = stream.read(
                    CHUNK_SIZE,
                    exception_on_overflow=False
                )

                if not data:
                    continue

                if recognizer.AcceptWaveform(data):

                    result = json.loads(
                        recognizer.Result()
                    )

                    text = result.get(
                        "text",
                        ""
                    ).strip()

                    if text:
                        last_text = text
                        break

            if not last_text:

                result = json.loads(
                    recognizer.FinalResult()
                )

                last_text = result.get(
                    "text",
                    ""
                ).strip()

        finally:

            stream.stop_stream()
            stream.close()

        if last_text:
            print(
                f"👤 You: {last_text}"
            )

            return last_text

        print("No speech detected.")

        return None

    def close(self):

        try:
            self.audio.terminate()
        except Exception:
            pass