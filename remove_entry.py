# Code to remove entries
import os
import sys
import shutil
import subprocess
import re

JSON_FOLDER = 'jsonFiles'
REMOVED_FOLDER = 'removedEntries'

# Find issues with label "remove entry"
def get_folder_name_from_title(issue_title):
    if ':' in issue_title: # Get entry name after the colon from the issue title
        folder_base = issue_title.split(':', 1)[1].strip()
    else:
        folder_base = issue_title.strip()
    # Sanitize to match folder naming convention
    folder_name = re.sub(r'[^A-Za-z0-9_\-]', '_', folder_base)
    return folder_name

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: remove_entry.py <issue_title>")
        sys.exit(1)

    issue_title = sys.argv[1]
    # Use the title of the issue to find the associated folder in JsonFiles
    folder_name = get_folder_name_from_title(issue_title)
    src_path = os.path.join(JSON_FOLDER, folder_name)
    dst_path = os.path.join(REMOVED_FOLDER, folder_name)

    if not os.path.exists(src_path):
        print(f"Folder {src_path} does not exist.")
        sys.exit(1)

    os.makedirs(REMOVED_FOLDER, exist_ok=True)
    # Move that folder into folder "removedEntries"
    shutil.move(src_path, dst_path)
    print(f"Moved {src_path} to {dst_path}")

    # Update the BioEco CSV list and sitemap
    subprocess.run([sys.executable, "collectNamesTo_csv.py"], check=True)
    subprocess.run([sys.executable, "generate_sitemap.py"], check=True)
