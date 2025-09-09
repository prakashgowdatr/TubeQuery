import os
from pathlib import Path
import yt_dlp

def download_audio(yt_url):
    """
    Downloads the audio in .wav format from the given YouTube URL and returns the filepath.
    """

    # Create a directory to save the downloaded audio files
    output_dir = "downloaded_files"
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # yt-dlp configuration
    ydl_config = {
        "format": "bestaudio/best",  # Best audio quality available
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # Use FFmpeg for audio extraction
                "preferredcodec": "wav",     # Save as wav format
                "preferredquality": "192",   # Optional, relevant for codecs like mp3
            }
        ],
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),  # Save file with title as name
        "verbose": True  # Show download progress in output
    }

    print(f"Downloading audio from {yt_url}")

    # Attempt to download the audio
    try:
        with yt_dlp.YoutubeDL(ydl_config) as ydl:
            info_dict = ydl.extract_info(yt_url, download=True)  # Extract metadata and download
            filename = os.path.join(output_dir, f"{info_dict['title']}.wav")
            print(f"Download successful!")
            return filename  # Return the final filename with relative path
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None  # Return None if download fails