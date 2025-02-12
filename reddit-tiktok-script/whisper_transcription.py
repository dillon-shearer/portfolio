"""
whisper_transcription.py

This module transcribes an audio file to an SRT file using OpenAI's Whisper API.
It calls openai.audio.transcriptions.create() with the "whisper-1" model and requests a verbose JSON
response with timestamp granularity (e.g. word-level). When word-level data is available, words are grouped
into subtitle entries that contain at most MAX_CHARS characters (including spaces). If word-level data is not available,
the segment's text is split by whitespace and grouped similarly.
Each subtitle entry will contain up to MAX_CHARS characters.

Usage examples:
    # Transcribe audio (e.g., test_audio.mp3) and output a raw SRT file:
    python whisper_transcription.py --audio_file test_audio.mp3

    # You can override the output filename and granularity:
    python whisper_transcription.py --audio_file test_audio.mp3 --srt_output my_subtitles.srt --granularity word

Dependencies:
    - openai (install via: pip install openai)
"""

import argparse
import openai
import json
import os

# Retrieve the OpenAI API key from the environment or prompt for it.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    OPENAI_API_KEY = input("Enter your OpenAI API key: ")

# Set the API key on the module.
openai.api_key = OPENAI_API_KEY

def format_time(seconds):
    """Convert seconds (float) to SRT timestamp format."""
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds % 60)
    m = int(seconds // 60 % 60)
    h = int(seconds // 3600)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def format_transcription(transcription, granularity):
    """
    Convert the transcript JSON into an SRT-formatted string.
    When word-level timestamps are available, words are grouped together until the total number
    of characters (including spaces) would exceed MAX_CHARS, then that group is output as one subtitle entry.
    If word-level data is not available, the segment's text is split by whitespace and grouped similarly.
    
    Args:
        transcription (dict): The verbose JSON transcript.
        granularity (list): The granularity used (e.g. ["word"]).
    
    Returns:
        str: The SRT content.
    """
    if not transcription:
        return "Failed to transcribe audio."
    
    MAX_CHARS = 25  # maximum characters per subtitle entry (including spaces)
    
    # If no "segments" key or it's empty, but "words" exists at the top level,
    # create a single segment from the top-level words.
    segments = transcription.get("segments", [])
    if not segments and "words" in transcription:
        segments = [{
            "words": transcription["words"],
            "start": 0,
            "end": transcription.get("duration", 0),
            "text": transcription.get("text", "")
        }]
    
    srt_lines = []
    subtitle_index = 1
    for seg in segments:
        if "words" in seg and seg["words"]:
            words = seg["words"]
            group = []
            group_text = ""
            group_start = None
            for word in words:
                current_word = word.get("word", "")
                # If the group is empty, start a new group.
                if not group:
                    group = [word]
                    group_text = current_word
                    group_start = word["start"]
                else:
                    tentative_text = group_text + " " + current_word
                    if len(tentative_text) > MAX_CHARS:
                        # Output the current group.
                        group_end = group[-1]["end"]
                        srt_lines.append(f"{subtitle_index}")
                        srt_lines.append(f"{format_time(group_start)} --> {format_time(group_end)}")
                        srt_lines.append(group_text)
                        srt_lines.append("")  # blank line
                        subtitle_index += 1
                        # Start a new group with the current word.
                        group = [word]
                        group_text = current_word
                        group_start = word["start"]
                    else:
                        group.append(word)
                        group_text = tentative_text
            # Output any remaining group.
            if group:
                group_end = group[-1]["end"]
                srt_lines.append(f"{subtitle_index}")
                srt_lines.append(f"{format_time(group_start)} --> {format_time(group_end)}")
                srt_lines.append(group_text)
                srt_lines.append("")
                subtitle_index += 1
        else:
            # Fallback: use the segment text, split by whitespace, and group words similarly.
            text = seg.get("text", "")
            word_list = text.split()
            if not word_list:
                continue
            seg_start = seg.get("start", 0)
            seg_end = seg.get("end", seg_start)
            # Group words until adding another word would exceed MAX_CHARS.
            groups = []
            current_group = []
            current_group_text = ""
            for word in word_list:
                if not current_group:
                    current_group = [word]
                    current_group_text = word
                else:
                    tentative_text = current_group_text + " " + word
                    if len(tentative_text) > MAX_CHARS:
                        groups.append(current_group)
                        current_group = [word]
                        current_group_text = word
                    else:
                        current_group.append(word)
                        current_group_text = tentative_text
            if current_group:
                groups.append(current_group)
            num_groups = len(groups)
            group_duration = (seg_end - seg_start) / num_groups if num_groups > 0 else 0
            current_time = seg_start
            for group in groups:
                group_text = " ".join(group)
                start_time = format_time(current_time)
                end_time = format_time(current_time + group_duration)
                srt_lines.append(f"{subtitle_index}")
                srt_lines.append(f"{start_time} --> {end_time}")
                srt_lines.append(group_text)
                srt_lines.append("")
                subtitle_index += 1
                current_time += group_duration
    return "\n".join(srt_lines)

def transcribe_audio(file_path, output_file, granularity=["word"]):
    """
    Transcribe the audio file using OpenAI's Whisper API with the new interface.
    This function writes the SRT content (grouping words up to MAX_CHARS per entry) to the specified output file.
    
    Args:
        file_path (str): Path to the input audio file (e.g., MP3).
        output_file (str): Path to save the raw SRT file.
        granularity (list): List of timestamp granularities (default: ["word"]).
    
    Returns:
        dict: The transcript as a dictionary (verbose JSON format) or None if an error occurred.
    """
    try:
        with open(file_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                response_format="verbose_json",
                timestamp_granularities=granularity
            )
        if hasattr(transcript, "to_dict"):
            transcript = transcript.to_dict()
        srt_content = format_transcription(transcript, granularity)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(srt_content)
        return transcript
    except Exception as e:
        print("An error occurred:", e)
        return None

def reformat_and_time_subtitles(input_file, output_file, max_length, min_display_time=1500):
    """
    Reformat the SRT file to produce the FINAL SRT.
    Since our transcribe_audio() already produces grouped subtitles,
    this function simply copies the content from the input file to the output file.
    
    Args:
        input_file (str): Path to the raw SRT file.
        output_file (str): Path to save the final SRT file.
        max_length (int): Maximum allowed characters per subtitle line (not used in this version).
        min_display_time (int): Minimum display time per subtitle segment in milliseconds (not used here).
    
    Returns:
        str: Path to the saved final SRT file.
    """
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Reformatted subtitles saved to {output_file}")
        return output_file
    except Exception as e:
        print("An error occurred during reformatting:", e)
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe an audio file to an SRT using OpenAI's Whisper API with word-level granularity, grouping words until 30 characters max per subtitle."
    )
    parser.add_argument("--audio_file", required=True, help="Path to the input audio file (e.g., MP3).")
    parser.add_argument("--granularity", nargs="+", default=["word"],
                        help="Timestamp granularities (e.g., 'word').")
    parser.add_argument("--srt_output", default="output.srt",
                        help="Path to save the raw SRT file (default: output.srt).")
    args = parser.parse_args()

    transcript = transcribe_audio(args.audio_file, args.srt_output, args.granularity)
    if transcript is None:
        print("Transcription failed.")
        return

    # For debugging: print the raw JSON response.
    print(json.dumps(transcript, indent=2))
    
    final_srt_output = args.srt_output.replace(".srt", "_final.srt")
    reformat_and_time_subtitles(args.srt_output, final_srt_output, max_length=50)
    print(f"Final SRT file saved to {final_srt_output}")

if __name__ == "__main__":
    main()