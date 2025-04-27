from moviepy import VideoFileClip
import subprocess
from contextlib import contextmanager
import os
import sys


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def resize_video(input_file, output_file, log_level, start_time=0, end_trim=0):
    with suppress_stdout():
        with VideoFileClip(input_file) as video:
            duration = video.duration

    trimmed_duration = duration - start_time - end_trim

    # Construct the FFmpeg command
    command = [
        "ffmpeg",
        "-ss", str(start_time),  # Seek to start_time seconds into the input before decoding (fast skip to start)
        "-i", input_file,  # Input file path
        "-t", str(trimmed_duration),  # Limit the output duration to trimmed_duration seconds
        "-vf", "scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
        # -vf applies a video filter:
        #    1. scale=1080:-2 -> Resize video to 1080 pixels wide, height auto-scaled to preserve aspect ratio (height divisible by 2)
        #    2. pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black -> Pad the video to 1080x1920 (portrait format), centering it with black bars
        "-c:v", "h264_nvenc",  # Set the video codec to NVIDIA GPU-based H.264 encoder (h264_nvenc)
        "-preset", "fast",  # Use the "fast" encoding preset (controls compression speed vs. efficiency tradeoff)
        "-crf", "23",  # Set Constant Rate Factor to 23 (lower means better quality; 23 is a good default)
        "-v", log_level,  # Set verbosity level for ffmpeg logs (e.g., quiet, error, warning, info, verbose, debug)
        output_file,  # Output file path
    ]

    # Run the command
    try:
        subprocess.run(command, check=True)
        print(f"Saved: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while processing video: {e}")
