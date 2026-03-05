import whisper
import imageio_ffmpeg
import subprocess
import numpy as np
import soundfile as sf
import os

speech_model = whisper.load_model("base")

def extract_audio(video_path, audio_path="temp_audio.wav"):
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    subprocess.run([
        ffmpeg_exe,
        "-i", video_path,
        "-ac", "1",
        "-ar", "16000",
        audio_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return audio_path


def video_to_text(video_path: str):
    audio_path = extract_audio(video_path)

    audio, sr = sf.read(audio_path)

    # mono convert
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)

    # ⭐ CRITICAL FIX
    audio = audio.astype(np.float32)

    result = speech_model.transcribe(audio)

    os.remove(audio_path)

    return result["text"]