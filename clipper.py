import os
import subprocess


def clip_video(
    input_file, output_dir, log_level, segment_duration=90, font_path="Arial.otf"
):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "ffprobe",
        "-i", input_file,  # Input file path to analyze
        "-show_entries", "format=duration",  # Only show the 'duration' field from the file's format metadata (ignore all other details)
        "-v", log_level,  # Set verbosity level for ffprobe logs (e.g., quiet, error, warning, info, verbose, debug)
        "-of", "csv=p=0",  # Set output format to CSV (comma-separated values)
        # p=0 -> "print no column names", so only the raw duration number is output
    ]

    # Get the video duration in seconds
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        total_duration = int(float(result.stdout.strip()))  # Convert to integer seconds
    except Exception as e:
        print(f"Error getting video duration: {e}")
        exit(1)

    part_number = 1
    start_time = 0

    while start_time < total_duration:
        output_file = os.path.join(
            output_dir,
            f"{os.path.splitext(os.path.basename(input_file))[0]} pt {part_number}.mp4",
        )

        command = [
            "ffmpeg",
            "-i", input_file,  # Input video file path
            "-vf", f"drawtext=fontfile={font_path}:text='Part {part_number}':x=(w-text_w)/2:y=h/4:fontsize=120:fontcolor=white",
            # -vf applies a video filter:
            #   drawtext -> Draw text on the video
            #     - fontfile={font_path} -> Path to the font file to use
            #     - text='Part {part_number}' -> The text to draw (e.g., "Part 1", "Part 2", etc.)
            #     - x=(w-text_w)/2 -> Center the text horizontally
            #     - y=h/4 -> Position the text at 1/4 of the video height from the top
            #     - fontsize=120 -> Set font size
            #     - fontcolor=white -> Set text color to white
            "-c:v", "h264_nvenc",  # Set the video codec to NVIDIA GPU-based H.264 encoder (h264_nvenc)
            "-preset", "fast",  # Use "fast" encoding preset (balances speed and compression efficiency)
            "-c:a", "aac",  # Set the audio codec to AAC (Advanced Audio Codec)
            "-b:a", "128k",  # Set the audio bitrate to 128 kbps
            "-movflags", "+faststart",  # Optimize MP4 file for streaming (moves metadata to the beginning of the file)
            "-t", str(segment_duration),  # Limit the output to segment_duration seconds long
            "-ss", str(start_time),
            # Seek to start_time seconds into the input before starting output
            # (Note: -ss after -i -> slower, frame-accurate seeking)
            "-v", log_level,  # Set the ffmpeg log verbosity (quiet, error, warning, info, etc.)
            output_file,  # Output file path
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Saved: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error processing part {part_number}: {e}")
            break

        start_time += segment_duration
        part_number += 1

    print("Video splitting and text addition completed!")
