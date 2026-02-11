import whisper
import numpy as np

model = whisper.load_model("tiny")  # fast for commands

def transcribe(audio: np.ndarray) -> str:
    # 1️⃣ Flatten (N,1) → (N,)
    if audio.ndim > 1:
        audio = audio.squeeze()

    # 2️⃣ Convert int16 → float32
    audio = audio.astype(np.float32)

    # 3️⃣ Normalize to [-1, 1]
    audio /= 32768.0

    # 4️⃣ Trim near-zero silence at the end (OPTIONAL but recommended)
    energy = np.abs(audio)
    last = np.where(energy > 0.01)[0]
    if len(last) > 0:
        audio = audio[: last[-1] + 1]

    # 5️⃣ Transcribe
    result = model.transcribe(
        audio,
        language="en",
        beam_size=1,
        temperature=0,
        fp16=False
    )

    return result["text"].strip()
