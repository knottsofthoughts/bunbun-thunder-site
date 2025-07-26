import subprocess
import os
import shutil

def convert_wma_to_wav(input_path: str) -> str:
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg not found in PATH. Please install it and try again.")

    base, _ = os.path.splitext(input_path)
    output_path = base + ".wav"
    subprocess.run(
        ["ffmpeg", "-y", "-i", input_path, "-ar", "44100", "-ac", "2", output_path],
        check=True
    )
    return output_path
