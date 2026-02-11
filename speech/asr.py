import whisper
import tempfile
import os

model = whisper.load_model("tiny")


def transcribe(audio_bytes: bytes) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp.write(audio_bytes)
    tmp.close()  # IMPORTANT on Windows

    try:
        result = model.transcribe(
            tmp.name,
            language="en",
            beam_size=1,
            temperature=0,
            fp16=False,
        )
    finally:
        os.remove(tmp.name)

    return result["text"].strip()
