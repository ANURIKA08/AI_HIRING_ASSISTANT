import sounddevice as sd
import scipy.io.wavfile as wav
import whisper
import numpy as np
import os
import tempfile


# Load Whisper model once
whisper_model = None


def get_whisper_model():
    global whisper_model
    if whisper_model is None:
        print("Loading Whisper model (first time takes 1-2 minutes)...")
        whisper_model = whisper.load_model("base")
        print("Whisper model loaded!")
    return whisper_model


def record_audio(duration=30, sample_rate=16000):
    """
    Record audio from microphone
    Input:  duration in seconds
    Output: audio file path
    """
    print(f"Recording for {duration} seconds... Speak now!")

    # Record audio
    audio_data = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype=np.int16
    )
    sd.wait()  # Wait for recording to finish
    print("Recording complete!")

    # Save to temp file
    temp_path = tempfile.mktemp(suffix='.wav')
    wav.write(temp_path, sample_rate, audio_data)

    return temp_path


def transcribe_audio(audio_path: str) -> str:
    """
    Convert audio to text using Whisper
    Input:  path to .wav file
    Output: transcribed text
    """
    if not os.path.exists(audio_path):
        return ""

    model = get_whisper_model()
    result = model.transcribe(audio_path)
    text = result['text'].strip()

    # Clean up temp file
    try:
        os.remove(audio_path)
    except:
        pass

    return text


def record_and_transcribe(duration=30) -> str:
    """
    Main function - record and transcribe in one step
    Input:  duration in seconds
    Output: transcribed text
    """
    audio_path = record_audio(duration)
    text = transcribe_audio(audio_path)
    print(f"You said: {text}")
    return text


# ---------- TEST IT ----------
if __name__ == "__main__":
    print("Testing Voice Interview...")
    print("This will record 5 seconds of audio")
    text = record_and_transcribe(duration=5)
    print(f"Transcribed: {text}")