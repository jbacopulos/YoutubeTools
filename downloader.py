from googleapiclient.discovery import build
import isodate
import os
import yt_dlp


def download(url):
    # Prepare the download options
    ydl_opts = {
        "outtmpl": "./downloads/%(title)s.%(ext)s",  # Save location and filename format
        "format": "bestvideo+bestaudio/best",  # Best video and audio
        "merge_output_format": "mp4",  # Merge into mp4 if needed
        "quiet": True,  # Don't spam the console
    }

    # Create downloads directory if it doesn't exist
    os.makedirs("./downloads", exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # Get the filename that was downloaded
        file_name = ydl.prepare_filename(info)
        file_name = os.path.basename(file_name)  # Only filename, not full path
        return file_name


def get_recent_videos(channel_id, api_key, max_results=10):
    # Build the YouTube API client
    youtube = build("youtube", "v3", developerKey=api_key)

    # Get the most recent videos from the channel
    search_response = (
        youtube.search()
        .list(
            part="id",
            channelId=channel_id,
            maxResults=max_results,
            order="date",
            type="video",
        )
        .execute()
    )

    video_urls = []
    for item in search_response["items"]:
        video_id = item["id"]["videoId"]

        # Fetch video details to filter out Shorts
        video_response = (
            youtube.videos().list(part="contentDetails", id=video_id).execute()
        )

        duration = video_response["items"][0]["contentDetails"]["duration"]
        duration_seconds = isodate.parse_duration(duration).total_seconds()

        if duration_seconds > 60:
            video_urls.append(f"https://www.youtube.com/watch?v={video_id}")

    return video_urls
