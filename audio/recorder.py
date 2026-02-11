import sounddevice as sd
import numpy as np
import time

SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 300
SILENCE_DURATION = 1.0
CHUNK_DURATION = 0.1
MIN_RECORD_SECONDS = 5.0

def record_until_silence():
    frames = []
    silent_chunks = 0

    chunk_size = int(SAMPLE_RATE * CHUNK_DURATION)
    min_chunks = int(MIN_RECORD_SECONDS / CHUNK_DURATION)
    max_silent_chunks = int(SILENCE_DURATION / CHUNK_DURATION)

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16") as stream:
        while True:
            chunk, _ = stream.read(chunk_size)
            frames.append(chunk)

            volume = np.abs(chunk).mean()

            if len(frames) >= min_chunks:
                if volume < SILENCE_THRESHOLD:
                    silent_chunks += 1
                else:
                    silent_chunks = 0

                if silent_chunks >= max_silent_chunks:
                    break

    return np.concatenate(frames)
