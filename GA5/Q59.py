import os, json, re
import tempfile
import hashlib
from pathlib import Path
from pydub import AudioSegment
import whisper

def execute(question: str, parameter, file_bytes = None):
    #temp_dir = tempfile.mkdtemp()
    input_file = Path(__file__).parent / "audio.mp3"
    output_file = Path(__file__).parent / "trimmed_audio.mp3"
    
    start_time, end_time = get_audio_time(question)
    trimmed_file = trim_audio(input_file, start_time=start_time, end_time=end_time, output_file= output_file)
    transcript = transcribe_audio(trimmed_file)
    return str(transcript).strip()


def trim_audio(input_file, start_time, end_time, output_file="trimmed_audio.mp3"):
    """Trims an audio file from start_time to end_time and saves it."""
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Audio file not found: {input_file}")

    audio = AudioSegment.from_file(input_file, format="mp3")
    trimmed_audio = audio[start_time * 1000:end_time * 1000]  # Convert to milliseconds
    trimmed_audio.export(output_file, format="mp3")

    print(f"Trimmed audio saved: {output_file}")
    return output_file

def transcribe_audio(audio_file, model_size="small"):
    """Transcribes the given audio file using OpenAI Whisper."""
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Trimmed audio file not found: {audio_file}")

    model = whisper.load_model(model_size)
    # result = model.transcribe(audio_file)
    audio_file = Path(audio_file)  # Path object
    result = model.transcribe(str(audio_file))  # Convert to string ✅
    return result["text"]

def get_audio_time(question):
    matches = re.findall(r"between (\d+\.?\d*) and (\d+\.?\d*) seconds", question)
    # Take the last time range if there are multiple matches
    last_time_range = matches[-1] if matches else None
    start_time = float(last_time_range[0])
    end_time = float(last_time_range[1])

    return start_time, end_time