"""
tts_elevenlabs.py

This module generates a TTS voiceover using the ElevenLabs API.
It converts input text into an MP3 audio file and can be run as a standalone script
or imported into your pipeline.

Usage:
    python tts_elevenlabs.py --text "Your text here" --output_file output_audio.mp3

Alternatively, you can specify a file containing the text:
    python tts_elevenlabs.py --text_file input.txt --output_file output_audio.mp3

Dependencies:
    - requests (install via: pip install requests)
"""

import argparse
import requests
import os

# Retrieve API key and Voice ID from environment variables.
API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    API_KEY = input("Enter your ElevenLabs API key: ")

VOICE_ID = "pNInz6obpgDQGcFmaJgB"

def generate_voiceover_elevenlabs(text, output_file):
    """
    Generate a TTS voiceover using the ElevenLabs API.
    Saves the resulting audio (MP3) to output_file.
    
    Args:
        text (str): The text to convert to speech.
        output_file (str): Path where the output MP3 will be saved.
    
    Returns:
        str: The path to the saved audio file.
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"TTS audio saved to {output_file}")
        return output_file
    else:
        raise Exception(f"ElevenLabs TTS error: {response.status_code} {response.text}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate a TTS voiceover using the ElevenLabs API and save the audio to an MP3 file."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text', type=str, help="The text to convert to speech.")
    group.add_argument('--text_file', type=str, help="Path to a file containing text to convert to speech.")
    
    parser.add_argument('--output_file', type=str, default="output_audio.mp3",
                        help="Path to save the output MP3 file (default: output_audio.mp3)")
    
    args = parser.parse_args()
    
    # Determine the text input
    if args.text_file:
        try:
            with open(args.text_file, "r", encoding="utf-8") as f:
                text = f.read().strip()
        except Exception as e:
            raise Exception(f"Error reading text file {args.text_file}: {e}")
    else:
        text = args.text

    if not text:
        raise Exception("No text provided for TTS generation.")

    # Generate the TTS audio using the hard-coded API_KEY and VOICE_ID
    generate_voiceover_elevenlabs(text, args.output_file)

if __name__ == "__main__":
    main()