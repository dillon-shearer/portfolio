"""
youtube_downloader.py

This script downloads a YouTube video using yt-dlp and then processes it with FFmpeg
to create vertical (9:16) clips. It will slice the downloaded video into multiple
4‑minute segments (dropping any final segment that is less than 4 minutes) and then
delete the original downloaded video.

Usage:
    python youtube_downloader.py --url "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

Dependencies:
    - yt-dlp (install via: pip install yt-dlp)
    - FFmpeg (must be installed and available in your system's PATH)
    - ffprobe (comes with FFmpeg)
"""

import os
import subprocess
import argparse
import math
import yt_dlp

def download_video(url, output_dir, cookies_file=None):
    """
    Download a YouTube video using yt-dlp.
    
    Args:
        url (str): YouTube video URL.
        output_dir (str): Directory to save the downloaded video.
        cookies_file (str): (Optional) Path to a cookies.txt file.
        
    Returns:
        str: Full path to the downloaded video file.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"Downloading video from: {url}")
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'merge_output_format': 'mp4',
        # Set a common user-agent
        'http_headers': {
            'User-Agent': ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/92.0.4515.131 Safari/537.36")
        }
    }
    if cookies_file:
        ydl_opts['cookies'] = cookies_file

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
        except Exception as e:
            raise Exception(f"yt-dlp error: {e}")
        filename = ydl.prepare_filename(info)
        print(f"Downloaded video to: {filename}")
        return filename

def get_video_duration(input_file):
    """
    Use ffprobe to get the total duration (in seconds) of the input video.
    """
    command = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_file
    ]
    try:
        output = subprocess.check_output(command).strip()
        return float(output)
    except Exception as e:
        raise Exception(f"Error getting video duration: {e}")

def process_video_to_vertical_clip(input_file, output_file, start_time=0, duration=240):
    """
    Process a downloaded video into a vertical 9:16 clip using FFmpeg.
    
    The FFmpeg command does the following:
      - Uses -ss to seek to the specified start time.
      - Crops the video: computes crop width as (input height * 9/16) and centers it horizontally.
      - Scales the cropped video to 1080x1920.
      - Trims the clip to the specified duration (in seconds).
      - Removes the audio.
    
    Args:
        input_file (str): Path to the downloaded video.
        output_file (str): Path to save the processed vertical clip.
        start_time (int or float): Start time in seconds for this segment.
        duration (int): Duration (in seconds) for the output clip (default: 240 seconds).
    """
    # Define the crop filter.
    crop_filter = "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920"
    
    command = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-i", input_file,
        "-vf", crop_filter,
        "-t", str(duration),
        "-an",  # Remove audio
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        output_file
    ]
    
    print("Running FFmpeg command:")
    print(" ".join(command))
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg error: {e}")
    
    print(f"Processed vertical clip saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Download a YouTube video using yt-dlp and process it into vertical (9:16) 4‑minute clips."
    )
    parser.add_argument('--url', type=str, required=True,
                        help="YouTube video URL to download and process.")
    parser.add_argument('--output_dir', type=str, default="downloads",
                        help="Directory to store the downloaded video. (default: downloads)")
    parser.add_argument('--clip_dir', type=str, default="processed_clips",
                        help="Directory to store the processed vertical clips. (default: processed_clips)")
    parser.add_argument('--duration', type=int, default=240,
                        help="Duration (in seconds) of each output clip. (default: 240 seconds)")
    parser.add_argument('--cookies', type=str, default=None,
                        help="(Optional) Path to a cookies.txt file to bypass restrictions.")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.clip_dir, exist_ok=True)

    try:
        # Download the video
        downloaded_file = download_video(args.url, args.output_dir, cookies_file=args.cookies)
        base_name = os.path.splitext(os.path.basename(downloaded_file))[0]

        # Get the total duration of the downloaded video
        total_duration = get_video_duration(downloaded_file)
        print(f"Total video duration: {total_duration:.2f} seconds")

        # Determine the number of full 4‑minute segments available.
        num_clips = math.floor(total_duration / args.duration)
        if num_clips < 1:
            print("Video is shorter than the required clip duration. Dropping this video.")
            return

        print(f"Extracting {num_clips} full clip(s) of {args.duration} seconds each.")
        for i in range(num_clips):
            start_time = i * args.duration
            output_file = os.path.join(args.clip_dir, f"{base_name}_vertical_clip_{i+1}.mp4")
            process_video_to_vertical_clip(downloaded_file, output_file, start_time=start_time, duration=args.duration)
        
        # Delete the downloaded video after processing the clips
        try:
            os.remove(downloaded_file)
            print(f"Deleted downloaded file: {downloaded_file}")
        except Exception as e:
            print(f"Could not delete downloaded file: {downloaded_file}. Error: {e}")
            
    except Exception as e:
        print(f"Error processing URL {args.url}: {e}")

if __name__ == "__main__":
    main()