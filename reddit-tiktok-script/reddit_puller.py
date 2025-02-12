"""
reddit_puller.py

This module fetches multiple Reddit stories from a specified subreddit,
cleans the text, and saves each story to a text file in a designated folder.
It now fetches the top stories of the week and applies a stricter character
limit to keep the TTS content under roughly 4 minutes.
Usage:
    python reddit_puller.py --subreddit shortstories --story_count 3 --output_dir stories
"""

import os
import json
import re
import argparse
import praw

# Define text replacement rules
REPLACEMENTS = {
    r'\bAITA\b': 'A.I.T.A. ',
    r'\bAITAH\b': 'A.I.T.A. ',
    r'\bmum\b': 'mom',
    r'\bdickhead\b': 'unpleasant person',
    r'\bdick\b': 'peepee',
    r'\bbitch\b': 'jerk',
    r'\bfucking\b': 'fudging',
    r'\bfuck\b': 'fudge',
    r'\bpussy\b': 'kitty cat',
    r'\bgoddamn\b': 'gosh darn',
    r'\bass\b': 'butt',
    r'\bshit\b': 'poo',
    r'\bpenis\b': 'peepee',
    r'\bvagina\b': 'kitty cat',
    r'�': ''
}

def clean_title(title):
    for pattern, replacement in REPLACEMENTS.items():
        title = re.sub(pattern, replacement, title, flags=re.IGNORECASE)
    return title

def clean_text(text):
    """Clean text using defined replacement rules."""
    for pattern, replacement in REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

def load_used_ids(filename):
    """Load list of used Reddit post IDs from a JSON file."""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_used_ids(filename, used_ids):
    """Save list of used Reddit post IDs to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(used_ids, f)

def fetch_multiple_reddit_stories(story_count=1, subreddit_name='aitah', used_ids_file='used_ids.json',
                                  number_of_posts=100, character_limit=2000, exclude_keyword='update'):
    """
    Fetch multiple Reddit stories from the specified subreddit.

    Args:
        story_count (int): Number of stories to fetch.
        subreddit_name (str): The subreddit to fetch stories from.
        used_ids_file (str): JSON file to track used post IDs.
        number_of_posts (int): Number of posts to consider from the listing.
        character_limit (int): Maximum allowed characters for combined title and content.
        exclude_keyword (str): Posts containing this keyword in the title are skipped.

    Returns:
        List[dict]: A list of dictionaries with keys 'title' and 'content'.
    """
    used_ids = load_used_ids(used_ids_file)

    reddit = praw.Reddit(
        client_id='ptQ5be3dLXvOLSK_liT3kQ',
        client_secret='OxpxGuX_UE7inkt0XbiUCBVBUYlbog',
        user_agent='script:dillon-tiktok-script:1.0 (by /u/Environmental_Fun_21)'
    )

    subreddit = reddit.subreddit(subreddit_name)
    stories = []

    # Use time_filter="week" to grab the top posts of the week
    for post in subreddit.top(time_filter="week", limit=number_of_posts):
        if exclude_keyword.lower() in post.title.lower():
            continue
        if post.id in used_ids:
            continue

        combined_text = post.title + "\n" + post.selftext
        if len(combined_text) > character_limit:
            continue

        used_ids.append(post.id)

        story = {
            "title": clean_text(post.title),
            "content": clean_text(post.selftext)
        }
        stories.append(story)

        if len(stories) >= story_count:
            break

    save_used_ids(used_ids_file, used_ids)
    return stories

def store_stories_to_files(stories, output_dir):
    """
    Store each story in a separate text file within the specified output directory.
    
    Each file will be named "story_<number>.txt" and will contain the title and content.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for idx, story in enumerate(stories, start=1):
        filename = os.path.join(output_dir, f"story_{idx}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Title: " + story["title"] + "\n\n")
            f.write("Content:\n" + story["content"])
        print(f"Saved story {idx} to {filename}")

def main():
    parser = argparse.ArgumentParser(
        description="Fetch multiple Reddit stories from a specified subreddit and save them as text files."
    )
    parser.add_argument('--subreddit', type=str, default='aitah',
                        help="Subreddit to fetch stories from (default: aitah)")
    parser.add_argument('--story_count', type=int, default=1,
                        help="Number of stories to fetch (default: 1)")
    parser.add_argument('--used_ids_file', type=str, default='used_ids.json',
                        help="File to store used post IDs (default: used_ids.json)")
    parser.add_argument('--number_of_posts', type=int, default=100,
                        help="Number of posts to consider from the listing (default: 100)")
    parser.add_argument('--character_limit', type=int, default=2000,
                        help="Maximum allowed characters for combined title and content (default: 2000)")
    parser.add_argument('--exclude_keyword', type=str, default='update',
                        help="Keyword to exclude posts (default: update)")
    parser.add_argument('--output_dir', type=str, default='stories',
                        help="Directory to store the fetched stories (default: stories)")
    args = parser.parse_args()

    stories = fetch_multiple_reddit_stories(
        story_count=args.story_count,
        subreddit_name=args.subreddit,
        used_ids_file=args.used_ids_file,
        number_of_posts=args.number_of_posts,
        character_limit=args.character_limit,
        exclude_keyword=args.exclude_keyword
    )

    if not stories:
        print("No suitable posts found.")
        return

    store_stories_to_files(stories, args.output_dir)

if __name__ == "__main__":
    main()
