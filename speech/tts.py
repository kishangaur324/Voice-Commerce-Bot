from gtts import gTTS
import tempfile
import os


def generate_speech(text: str) -> bytes:
    tts = gTTS(text=text, lang="en")

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    tmp.close()

    with open(tmp.name, "rb") as f:
        audio_bytes = f.read()

    os.remove(tmp.name)

    return audio_bytes
