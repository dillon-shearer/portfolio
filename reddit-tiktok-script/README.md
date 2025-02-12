# Reddit TikTok Script

## Overview
The Reddit TikTok Script is a Python-based pipeline that automates the creation of TikTok-ready videos from Reddit posts. It fetches content from your chosen subreddit, converts text to speech, transcribes the audio for subtitles, and then assembles a final video clip. This end-to-end solution helps you quickly generate engaging content for TikTok.

## Features
- **Reddit Content Fetching:** Pull trending or specific posts from any subreddit.
- **Text-to-Speech (TTS):** Convert post text into high-quality audio using ElevenLabs.
- **Audio Transcription:** Use OpenAI’s Whisper API to generate subtitles with word-level granularity.
- **Video Assembly:** Combine video clips, the generated audio, and subtitles into a final video.
- **Customizable Pipeline:** Easily tweak parameters (subreddit, batch count, test text) via command-line arguments.

## Getting Started

### Prerequisites
- Python 3.x
- API keys for:
  - ElevenLabs TTS
  - OpenAI (for Whisper transcription)
- Required Python libraries (listed in `requirements.txt`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/dillon-shearer/reddit-tiktok-script.git
   cd reddit-tiktok-script
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
For security and ease-of-use, the pipeline expects your API keys to be set as environment variables or stored in a `.env` file (if using [python-dotenv](https://pypi.org/project/python-dotenv/)):

```bash
export ELEVENLABS_API_KEY="your_elevenlabs_api_key"
export ELEVENLABS_VOICE_ID="your_elevenlabs_voice_id"
export OPENAI_API_KEY="your_openai_api_key"
```

Alternatively, create a `.env` file in the project root:

```dotenv
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_elevenlabs_voice_id
OPENAI_API_KEY=your_openai_api_key
```

### Usage
Run the pipeline with:

```bash
python pipeline.py --subreddit aitah --batch_count 1
```

For testing with custom text:

```bash
python pipeline.py --subreddit aitah --batch_count 1 --test_text "Your custom text here"
```

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/dillon-shearer/reddit-tiktok-script/issues) if you want to contribute.

## License
This project is licensed under the MIT License.
