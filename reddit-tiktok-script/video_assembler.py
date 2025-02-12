"""
video_assembler.py

This module assembles a final vertical video by combining a video clip, TTS audio,
and burning in subtitles using FFmpeg with:
  - A 1-second shift applied to the subtitles (via pre‑processing the SRT file)
  - A 1-second delay applied to the audio using the adelay filter
  - The -shortest flag so that the final output stops when the audio stream ends

It now also supports an optional cover-page overlay:
  - If --title_text is provided, a white textbox is drawn for the duration of the title TTS (determined automatically).
  - After the title overlay, the normal word-level subtitles are burned in.

Usage Examples:
  -- To specify a video file manually:
     python video_assembler.py --video_file processed_clips/85z7jqGAGcc_vertical_clip_1.mp4 \
       --audio_file testing.mp3 --subtitle_file testing_final.srt --output_file final_video.mp4 --start_time 0 \
       --title_text "Testing testing 1, 2, 3!"
  -- To auto-select the next unused video clip:
     python video_assembler.py --auto --video_dir processed_clips --video_prefix 85z7jqGAGcc \
       --audio_file testing.mp3 --subtitle_file testing_final.srt --output_file final_video.mp4 --start_time 0 \
       --title_text "Testing testing 1, 2, 3!"

Dependencies:
  - FFmpeg (must be installed and in your system's PATH)
  - ffprobe (comes with FFmpeg)
"""

import argparse
import subprocess
import os

def format_time(seconds):
    """Convert seconds (float) to SRT timestamp format."""
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds % 60)
    m = int(seconds // 60 % 60)
    h = int(seconds // 3600)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def convert_to_milliseconds(timestamp):
    """Convert an SRT timestamp (HH:MM:SS,ms) to milliseconds."""
    h, m, s = timestamp.split(':')
    s, ms = s.split(',')
    return int(h)*3600000 + int(m)*60000 + int(s)*1000 + int(ms)

def convert_to_timestamp(milliseconds):
    """Convert milliseconds to an SRT timestamp (HH:MM:SS,ms)."""
    hours = int(milliseconds / 3600000)
    minutes = int((milliseconds % 3600000) / 60000)
    seconds = int((milliseconds % 60000) / 1000)
    ms = int(milliseconds % 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"

def shift_subtitles(srt_file, offset, output_file):
    """
    Shift all subtitle timestamps in an SRT file by offset seconds.
    """
    with open(srt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if '-->' in line:
            parts = line.strip().split('-->')
            if len(parts) == 2:
                start_str = parts[0].strip()
                end_str = parts[1].strip()
                start_ms = convert_to_milliseconds(start_str) + int(offset * 1000)
                end_ms = convert_to_milliseconds(end_str) + int(offset * 1000)
                new_line = f"{convert_to_timestamp(start_ms)} --> {convert_to_timestamp(end_ms)}\n"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"Shifted subtitles saved to {output_file}")
    return output_file

def combine_video_audio_add_subtitles(video_file, audio_file, subtitle_file, output_file, start_time=0,
                                      title_text=None, title_duration=0):
    """
    Combine the video clip, TTS audio, and burn in subtitles using FFmpeg.
    
    - The SRT file is pre-processed to shift all subtitles by 1 second.
    - The audio is delayed by 1 second using the adelay filter.
    - If title_text and title_duration are provided, a cover-page overlay is applied
      using drawtext for frames where t < title_duration.
    - After title_duration, the subtitles (with word-level data) are enabled.
    
    Args:
        video_file (str): Path to the video clip file.
        audio_file (str): Path to the TTS audio file (MP3).
        subtitle_file (str): Path to the FINAL SRT subtitle file.
        output_file (str): Path to save the final video file.
        start_time (float): Start time offset (in seconds) for the video (default: 0).
        title_text (str): (Optional) Title text to display on the cover page.
        title_duration (float): (Optional) Duration (in seconds) for the title overlay.
    
    Returns:
        None. The final video is saved to output_file.
    """
    # Pre-process the subtitles: shift them by 1 second.
    shifted_sub_file = os.path.splitext(subtitle_file)[0] + "_shifted.srt"
    shift_subtitles(subtitle_file, 1.0, shifted_sub_file)
    
    # Get relative path for the shifted subtitles file.
    subs_path = os.path.relpath(shifted_sub_file, os.getcwd()).replace("\\", "/")
    
    filters = []
    
    # Build drawtext filter for title overlay, if title_text and title_duration are provided.
    if title_text and title_duration > 0:
        drawtext_filter = (
            f"drawtext=text='{title_text}':"
            "box=1:boxcolor=white@1.0:boxborderw=5:"
            "x=(w-text_w)/2:y=(h-text_h)/2:"
            "fontsize=48:fontcolor=black:"
            f"enable='lt(t,{title_duration})'"
        )
        filters.append(drawtext_filter)
        subtitles_enable = f"enable='gte(t,{title_duration})'"
    else:
        subtitles_enable = ""
    
    # Build subtitles filter.
    subtitles_filter = (
        f"subtitles='{subs_path}':force_style='Alignment=10,FontSize=16,"
        "PrimaryColour=&H00ffffff,OutlineColour=&H00000000,BackColour=&H80000000,"
        "BorderStyle=1,Outline=1.3,Shadow=1,MarginL=80,MarginR=80,MarginV=150,Spacing=1'"
    )
    if subtitles_enable:
        subtitles_filter += f":{subtitles_enable}"
    
    filters.append(subtitles_filter)
    
    filter_complex = f"[0:v]{','.join(filters)}[v]"
    
    # Construct the FFmpeg command with a 1-second audio delay.
    command = [
        "ffmpeg",
        "-ss", str(start_time),
        "-i", video_file,
        "-i", audio_file,
        "-filter_complex", f"{filter_complex};[1:a]adelay=1000|1000[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-strict", "experimental",
        "-shortest",
        output_file
    ]
    
    print("Running FFmpeg command:")
    print(" ".join(command))
    subprocess.run(command, check=True)
    print(f"Final video saved to {output_file}")
    
    # Cleanup: delete the original unshifted SRT file and rename the shifted file.
    try:
        os.remove(subtitle_file)
        os.rename(shifted_sub_file, subtitle_file)
        print(f"Replaced unshifted SRT with shifted SRT at {subtitle_file}")
    except Exception as e:
        print(f"Error during SRT cleanup: {e}")

def get_next_video(auto, video_dir, video_prefix, last_used_file, provided_video_file):
    """
    Determine the video file to use.
    
    If auto mode is enabled, read the last used index from last_used_file (defaulting to 0),
    increment it, construct the filename based on video_prefix and the naming convention,
    and update the file. Otherwise, return the provided video file.
    """
    if auto:
        if not video_prefix:
            raise ValueError("When using auto mode, --video_prefix is required.")
        if os.path.exists(last_used_file):
            try:
                with open(last_used_file, "r") as f:
                    last_used = int(f.read().strip())
            except Exception:
                last_used = 0
        else:
            last_used = 0
        next_index = last_used + 1
        video_file = os.path.join(video_dir, f"{video_prefix}_vertical_clip_{next_index}.mp4")
        if not os.path.exists(video_file):
            raise FileNotFoundError(f"Expected video file not found: {video_file}")
        with open(last_used_file, "w") as f:
            f.write(str(next_index))
        print(f"Auto-selected video file: {video_file}")
        return video_file
    else:
        if not provided_video_file:
            raise ValueError("Either provide a video file with --video_file or use --auto mode.")
        return provided_video_file

def main():
    parser = argparse.ArgumentParser(
        description="Assemble a final vertical video by combining a video clip, TTS audio, and burning in subtitles with an optional cover-page overlay for the title."
    )
    # Auto-selection arguments.
    parser.add_argument('--auto', action='store_true', help="Automatically select the next unused video clip.")
    parser.add_argument('--video_dir', type=str, default="processed_clips", help="Directory containing video clips (default: processed_clips).")
    parser.add_argument('--video_prefix', type=str, help="Prefix for video clip files (e.g., 85z7jqGAGcc). Required if --auto is set.")
    parser.add_argument('--last_used_file', type=str, default="last_used_clip.txt", help="File to store the last used clip index (default: last_used_clip.txt).")
    parser.add_argument('--video_file', type=str, help="Path to the video clip file (if not using auto-selection).")
    # Other necessary arguments.
    parser.add_argument('--audio_file', type=str, required=True, help="Path to the TTS audio file (MP3).")
    parser.add_argument('--subtitle_file', type=str, required=True, help="Path to the FINAL SRT subtitle file.")
    parser.add_argument('--output_file', type=str, required=True, help="Path to save the final video file.")
    parser.add_argument('--start_time', type=float, default=0, help="Start time offset (in seconds) for the video (default: 0).")
    # New cover-page overlay argument.
    parser.add_argument('--title_text', type=str, default="", help="Title text to display in the cover-page overlay (derived from the title TTS).")
    
    args = parser.parse_args()
    
    video_file = get_next_video(args.auto, args.video_dir, args.video_prefix, args.last_used_file, args.video_file)
    
    # Before assembling the final video, determine the title overlay duration.
    title_duration = 0
    if args.title_text:
        base_name = os.path.splitext(os.path.basename(args.audio_file))[0]
        title_audio_path = os.path.join(os.path.dirname(args.audio_file), f"{base_name}_title.mp3")
        if os.path.exists(title_audio_path):
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                title_audio_path
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                title_duration = float(result.stdout.strip())
                print(f"Measured title TTS duration: {title_duration:.2f} seconds")
            except Exception as e:
                print("Error measuring title TTS duration:", e)
        else:
            print(f"Title TTS audio file not found at {title_audio_path}. No cover-page overlay will be applied.")
    
    combine_video_audio_add_subtitles(video_file, args.audio_file, args.subtitle_file, args.output_file, 
                                      start_time=args.start_time, title_text=args.title_text, 
                                      title_duration=title_duration)
    
if __name__ == "__main__":
    main()