import os
import shutil
import re
from multiprocessing import Pool, cpu_count, freeze_support
from tqdm import tqdm

# Regex pattern to match the date in the filename
date_pattern = re.compile(r"(20\d{2})(0[1-9]|1[0-2])\d{2}")

# List of image and video file extensions
image_video_extensions = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".mp4",
    ".avi",
    ".mov",
    ".wmv",
    ".flv",
    ".mp",
)

# Set your source and destination paths
source_path = "G:/takeout/parsed"
destination_base_path = "G:/takeout/parsed"


def move_file(file_path):
    """
    Move a file from its current location to a new destination based on its extension and date in filename.

    Args:
        file_path (str): The current location of the file.
    """
    # Check if the file is an image or a video
    if file_path.lower().endswith(image_video_extensions):
        # Try to find a date in the filename
        match = date_pattern.search(os.path.basename(file_path))
        if match:
            # Extract the year and create a destination path
            year = match.group(1)
            destination_path = os.path.join(destination_base_path, year)
        else:
            # No date found, use the 'unknown' folder
            destination_path = os.path.join(destination_base_path, "unknown")
    else:
        # File is not an image or video, use the 'unknown' folder
        destination_path = os.path.join(destination_base_path, "unknown")

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    # Move the file if it's not already in the destination
    if os.path.join(destination_path, os.path.basename(file_path)) != file_path:
        shutil.move(
            file_path, os.path.join(destination_path, os.path.basename(file_path))
        )


def main():
    """
    Main function to move all files from the source path to the destination path based on their extension and date in filename.
    """
    all_files = []
    for root, dirs, files in os.walk(source_path):
        for file in files:
            all_files.append(os.path.join(root, file))

    # Create a progress bar
    pbar = tqdm(total=len(all_files))

    # Function to update the progress bar
    def update(*a):
        pbar.update()

    with Pool(processes=cpu_count()) as pool:
        for _ in pool.imap_unordered(move_file, all_files):
            update()

    # Close the progress bar
    pbar.close()


if __name__ == "__main__":
    freeze_support()
    main()
