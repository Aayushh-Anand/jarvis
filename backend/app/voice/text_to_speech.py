import pyttsx3


_engine = None


def get_engine():

    global _engine

    if _engine is None:

        _engine = pyttsx3.init()

        _engine.setProperty(
            "rate",
            175
        )

        _engine.setProperty(
            "volume",
            1.0
        )

    return _engine


def speak(text: str):

    if not text:
        return

    engine = get_engine()

    print(
        f"🔊 JARVIS speaking..."
    )

    engine.say(str(text))

    engine.runAndWait()