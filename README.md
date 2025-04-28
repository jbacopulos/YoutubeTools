# YouTube Tools

## Overview
This project uses Python to interact with the YouTube API, download videos, and perform video processing tasks.  
It requires some external libraries and tools to work properly.

---

## Python Packages

Install the required Python packages:

```bash
pip install python-dotenv google-api-python-client yt_dlp moviepy
```

Packages used:
- `dotenv` (`python-dotenv`) — for loading environment variables
- `googleapiclient.discovery` — to interact with the YouTube Data API
- `yt_dlp` — to download YouTube videos
- `moviepy` — for video editing
- `contextlib` — standard Python library for managing context (no installation needed)

---

## FFmpeg Requirement

**FFmpeg** is required for video processing.  
Follow the instructions below to install FFmpeg based on your operating system:

### Windows
1. Download FFmpeg from the official website: https://ffmpeg.org/download.html
2. Under "Get packages & executable files", choose a Windows build (e.g., from [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/)).
3. Extract the ZIP file.
4. Add the `bin` folder path to your **System Environment Variables** → **Path**.
5. Verify installation:
   ```bash
   ffmpeg -version
   ```

### macOS
Install FFmpeg using Homebrew:
```bash
brew install ffmpeg
```
Verify installation:
```bash
ffmpeg -version
```

### Linux (Ubuntu/Debian)
Install FFmpeg with:
```bash
sudo apt update
sudo apt install ffmpeg
```
Verify installation:
```bash
ffmpeg -version
```

---

## Environment Variables

You must create a `.env` file in the project root with the following content:

```
API_KEY=your_google_api_key_here
CHANNEL_ID=your_youtube_channel_id_here
```

- `API_KEY` — Google YouTube Data API v3 key
- `CHANNEL_ID` — ID of the YouTube channel you want to interact with

---

## Notes
- Make sure your API key has **YouTube Data API v3** enabled in the Google Cloud Console.
- FFmpeg must be correctly installed and added to your system PATH for the project to function properly.

---
