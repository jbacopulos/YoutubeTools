import os
import downloader
import resizer
import clipper
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    API_KEY = os.getenv("API_KEY")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    MAX_RESULTS = 1
    LOG_LEVEL = "fatal"

    video_urls = downloader.get_recent_videos(CHANNEL_ID, API_KEY, MAX_RESULTS)

    for url in video_urls:
        print(f"Downloading: {url}")
        file_name = downloader.download(url)

        print(f"Resizing: {file_name}")
        resizer.resize_video(
            input_file=f"{os.getcwd()}\\downloads\\{file_name}",
            output_file=f"{os.getcwd()}\\resized\\{file_name}",
            log_level=LOG_LEVEL,
        )

        print(f"Clipping: {file_name}")
        clipper.clip_video(
            input_file=f"{os.getcwd()}\\resized\\{file_name}",
            output_dir=f"{os.getcwd()}\\output",
            log_level=LOG_LEVEL,
        )
