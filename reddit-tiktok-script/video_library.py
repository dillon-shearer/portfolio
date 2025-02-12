import os
import re

# Set the library directory to where your processed video clips are stored.
LIBRARY_DIR = "processed_clips"
# File to store the last used video index.
LAST_USED_FILE = os.path.join(LIBRARY_DIR, "last_used_clip.txt")

def list_video_library(library_dir=LIBRARY_DIR, prefix="", extensions=(".mp4", ".mov", ".mkv")):
    """
    List all video files in the library that match the given prefix and extensions,
    sorted in ascending order based on the numeric portion in the filename.
    """
    if not os.path.isdir(library_dir):
        raise Exception(f"Library directory '{library_dir}' does not exist.")
    
    # List all files with the desired extensions.
    files = [f for f in os.listdir(library_dir) if f.lower().endswith(extensions)]
    
    # If a prefix is provided, filter to only include files that start with it.
    if prefix:
        files = [f for f in files if f.startswith(prefix)]
    
    # Define a helper function to extract a numeric index from the filename.
    def extract_number(filename):
        # Example filename: "85z7jqGAGcc_vertical_clip_1.mp4"
        # This regex looks for an underscore followed by one or more digits before a dot.
        match = re.search(r'_(\d+)\.', filename)
        return int(match.group(1)) if match else 0
    
    files.sort(key=extract_number)
    # Return full paths for each file.
    return [os.path.join(library_dir, f) for f in files]

def pick_video_from_library(prefix=""):
    """
    Pick the next video file sequentially from the library.
    
    Reads the last used index from LAST_USED_FILE (defaulting to 0 if not present),
    selects the next video from the sorted list, and updates LAST_USED_FILE.
    Cycles back to the first video when all have been used.
    
    Args:
        prefix (str): The prefix of the video files to select (e.g., "85z7jqGAGcc").
    
    Returns:
        str: Full path to the selected video file.
    """
    videos = list_video_library(prefix=prefix)
    if not videos:
        raise Exception("No video files found in the library.")
    
    # Read the last used index.
    if os.path.exists(LAST_USED_FILE):
        try:
            with open(LAST_USED_FILE, "r") as f:
                last_used = int(f.read().strip())
        except Exception:
            last_used = 0
    else:
        last_used = 0

    # Determine the next index (1-indexed).
    next_index = last_used + 1
    if next_index > len(videos):
        next_index = 1

    selected_video = videos[next_index - 1]

    # Update the last used index.
    with open(LAST_USED_FILE, "w") as f:
        f.write(str(next_index))

    return selected_video

if __name__ == "__main__":
    # For testing: provide your video prefix (e.g., "85z7jqGAGcc") to select from the library.
    video = pick_video_from_library(prefix="85z7jqGAGcc")
    print("Selected video:", video)