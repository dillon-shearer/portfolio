"""
pipeline.py

Usage:
  python pipeline.py --subreddit aitah --batch_count 7
  (By default, the pipeline fetches Reddit stories.)
  
  To test with your own text instead of pulling a Reddit story, use:
  python pipeline.py --subreddit aitah --batch_count 1 --test_text "testing word-level granularity with Whisper API"

This pipeline performs the following steps for each batch item:
  1. Fetches a Reddit story from the specified subreddit (unless --test_text is provided).
  2. Saves the story text to a file under the "data/text/{subreddit}" folder.
  3. Generates TTS audio (final MP3) from the story text using ElevenLabs.
  4. Transcribes the TTS audio using OpenAI’s Whisper API to produce a raw SRT.
  5. Reformats the raw SRT for proper on-screen display (producing the FINAL SRT).
  6. Picks a pre‑processed video clip from the library.
  7. Assembles the final video by combining the selected video clip, the TTS audio, and the FINAL SRT.
  8. Removes any intermediate files (only the FINAL SRT, FINAL MP3, and FINAL video remain).

Final outputs are organized as follows:
  - Story text: data/text/{subreddit}/
  - TTS audio (final MP3): data/audio/
  - Final SRT: data/srt/
  - Final video: data/final/
"""

import os
import datetime
import sys
from reddit_puller import fetch_multiple_reddit_stories
from tts_elevenlabs import generate_voiceover_elevenlabs
from whisper_transcription import transcribe_audio, reformat_and_time_subtitles
from video_library import pick_video_from_library
from video_assembler import combine_video_audio_add_subtitles

def run_pipeline_instance(batch_id, subreddit, test_text=None):
    base_dir = os.getcwd()
    
    # Define output directories.
    text_dir = os.path.join(base_dir, "data", "text", subreddit)
    audio_dir = os.path.join(base_dir, "data", "audio")
    srt_dir = os.path.join(base_dir, "data", "srt")
    final_video_dir = os.path.join(base_dir, "data", "final")
    
    # Create directories if they don't exist.
    for d in [text_dir, audio_dir, srt_dir, final_video_dir]:
        os.makedirs(d, exist_ok=True)
    
    # Use current date and sequential number for uniqueness.
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    base_name = f"{today_str}_{subreddit}_reddit_post_{batch_id}"
    
    print(f"\n--- Processing batch item {batch_id} for subreddit '{subreddit}' ---")
    
    # Step 1: Get the story text.
    if test_text:
        story_text = test_text
        print("Using test text provided via --test_text.")
    else:
        print("Fetching Reddit story...")
        posts = fetch_multiple_reddit_stories(subreddit_name=subreddit, used_ids_file="used_ids.json", story_count=1)
        if not posts:
            print("No valid Reddit post fetched. Exiting this instance.")
            return
        post = posts[0]
        story_text = f"{post['title']}\n\n{post['content']}"
    
    # Step 2: Save the story text to a file.
    text_file_path = os.path.join(text_dir, base_name + ".txt")
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(story_text)
    print(f"Saved story text to {text_file_path}")
    if not os.path.exists(text_file_path):
        print("Text file was not created.")
        sys.exit(1)
    
    # Step 3: Generate TTS audio using ElevenLabs.
    audio_file_path = os.path.join(audio_dir, base_name + ".mp3")
    generate_voiceover_elevenlabs(story_text, audio_file_path)
    if not os.path.exists(audio_file_path):
        print("Audio file was not created.")
        sys.exit(1)
    
    # Step 4: Transcribe the audio to generate a raw SRT.
    raw_srt_path = os.path.join(srt_dir, base_name + ".srt")
    transcribe_audio(audio_file_path, raw_srt_path)
    print(f"Raw SRT saved to {raw_srt_path}")
    if not os.path.exists(raw_srt_path):
        print("Raw SRT file was not created.")
        sys.exit(1)
    
    # Step 5: Reformat the SRT to produce the FINAL SRT.
    final_srt_path = os.path.join(srt_dir, base_name + "_final.srt")
    reformat_and_time_subtitles(raw_srt_path, final_srt_path, max_length=50)
    print(f"Final SRT saved to {final_srt_path}")
    if os.path.exists(raw_srt_path):
        os.remove(raw_srt_path)
        print(f"Removed raw SRT file {raw_srt_path}")
    if not os.path.exists(final_srt_path):
        print("Final SRT file is missing.")
        sys.exit(1)
    
    # Step 6: Pick a pre‑processed video clip from your library.
    video_file = pick_video_from_library(prefix="85z7jqGAGcc")
    print("Selected video clip:", video_file)
    if not os.path.exists(video_file):
        print("Selected video file does not exist.")
        sys.exit(1)
    
    # Step 7: Assemble the final video by combining video, audio, and FINAL SRT.
    final_video_path = os.path.join(final_video_dir, base_name + ".mp4")
    combine_video_audio_add_subtitles(video_file, audio_file_path, final_srt_path, final_video_path)
    print("Pipeline instance complete! Final video saved at:", final_video_path)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    import argparse
    parser = argparse.ArgumentParser(
        description="Run the full pipeline for generating final videos from Reddit stories. Use --batch_count to specify how many to run, --subreddit to select the subreddit, and optionally --test_text to provide custom text for testing."
    )
    parser.add_argument('--subreddit', type=str, default="aitah",
                        help="Subreddit to pull from (default: 'aitah').")
    parser.add_argument('--batch_count', type=int, default=1,
                        help="Number of videos to produce in one run (default: 1).")
    parser.add_argument('--test_text', type=str, default="",
                        help="(Optional) If provided, use this text instead of pulling a Reddit story for testing purposes.")
    args = parser.parse_args()
    
    for i in range(1, args.batch_count + 1):
        # If test_text is provided, pass it to the pipeline instance.
        if args.test_text:
            run_pipeline_instance(i, args.subreddit, test_text=args.test_text)
        else:
            run_pipeline_instance(i, args.subreddit)
    
if __name__ == "__main__":
    main()