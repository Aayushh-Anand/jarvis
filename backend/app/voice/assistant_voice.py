from app.voice.speech_to_text import (
    OfflineSpeechToText
)

from app.voice.text_to_speech import (
    speak
)

from app.ai.assistant import (
    ask_jarvis
)


class JarvisVoiceAssistant:

    def __init__(
        self,
        conversation_id: str = "voice-session"
    ):

        self.conversation_id = (
            conversation_id
        )

        self.stt = OfflineSpeechToText()

        self.running = False

    def start(self):

        self.running = True

        print()
        print("=" * 55)
        print("        J.A.R.V.I.S. VOICE SYSTEM")
        print("=" * 55)
        print()
        print("Voice mode: ONLINE")
        print("Speech recognition: OFFLINE")
        print("Computer control: OFFLINE")
        print("AI responses: GEMINI")
        print()
        print("Say 'exit' or 'quit' to stop.")
        print()
        print("=" * 55)

        speak(
            "Good evening. "
            "JARVIS voice system is ready."
        )

        while self.running:

            try:

                user_message = self.stt.listen(
                    timeout=10
                )

                if not user_message:
                    continue

                command = (
                    user_message
                    .strip()
                    .lower()
                )

                # -------------------------
                # EXIT COMMAND
                # -------------------------

                if command in {
                    "exit",
                    "quit",
                    "stop",
                    "goodbye",
                    "shutdown jarvis"
                }:

                    speak(
                        "Voice system shutting down."
                    )

                    self.running = False
                    break

                # -------------------------
                # JARVIS COMMAND
                # -------------------------

                print()
                print(
                    "JARVIS is processing..."
                )

                try:

                    response = ask_jarvis(
                        self.conversation_id,
                        user_message
                    )

                    print()
                    print(
                        f"JARVIS: {response}"
                    )

                    # Keep TTS concise enough
                    # for practical voice use.
                    speak(response)

                except Exception as e:

                    print(
                        "JARVIS ERROR:"
                    )

                    print(
                        f"{type(e).__name__}: {e}"
                    )

                    speak(
                        "I encountered an error "
                        "while processing that request."
                    )

            except KeyboardInterrupt:

                print()
                print(
                    "Voice assistant stopped."
                )

                self.running = False

            except Exception as e:

                print(
                    "VOICE LOOP ERROR:"
                )

                print(
                    f"{type(e).__name__}: {e}"
                )

        self.stop()

    def stop(self):

        self.running = False

        try:
            self.stt.close()
        except Exception:
            pass

        print()
        print(
            "J.A.R.V.I.S. voice system offline."
        )


def start_voice_assistant(
    conversation_id: str = "voice-session"
):

    assistant = JarvisVoiceAssistant(
        conversation_id=conversation_id
    )

    assistant.start()