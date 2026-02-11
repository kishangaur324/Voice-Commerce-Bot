import numpy as np
import sounddevice as sd
from kokoro import KPipeline

tts_pipeline = KPipeline(lang_code="a")

def speak(text: str):
    chunks = []
    for _, _, audio in tts_pipeline(text, voice="af_bella"):
        chunks.append(audio)

    final_audio = np.concatenate(chunks)
    sd.play(final_audio, samplerate=24000)
    sd.wait()
