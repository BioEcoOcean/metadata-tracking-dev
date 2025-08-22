import json
import os
import subprocess
from datetime import datetime

# Define constants
REPO_ORG = "BioEcoOcean"
REPO_NAME = "metadata-tracking-dev"
BRANCH = "refs/heads/main"  
JSON_FOLDER = "jsonFiles"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{REPO_ORG}/{REPO_NAME}/{BRANCH}/{JSON_FOLDER}"

def get_git_last_modified_date(file_path):
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"    ERROR getting git last modified date for {file_path}: {e}")
        return None

def get_frequency_from_file(freq_file_path):
    if os.path.exists(freq_file_path):
        try:
            with open(freq_file_path, "r", encoding="utf-8") as f:
                freq_data = json.load(f)
                return freq_data.get("frequency", "never")
        except Exception as e:
            print(f"    ERROR reading frequency from {freq_file_path}: {e}")
    return "never"

def generate_sitemap():
    """Generates a single sitemap for all .json files in the jsonFiles folder and its subfolders."""
    sitemap_entries = []

    # Traverse all subfolders and gather .json file data
    for root, dirs, files in os.walk(JSON_FOLDER):
        print(f"Checking folder: {root}")
        if "Example" in os.path.normpath(root).split(os.sep):
            continue  # Skip any folder named Example
        print(f"Checking folder: {root}")
        for file_name in files:
            if file_name.endswith(".json") and not file_name.endswith("_actions.json") and not file_name.endswith("_frequency.json"):
                folder_name = os.path.splitext(file_name)[0]
                main_json_path = os.path.join(root, f"{folder_name}.json")
                actions_json_path = os.path.join(root, f"{folder_name}_actions.json")
                freq_json_path = os.path.join(root, f"{folder_name}_frequency.json")
                relative_folder = os.path.relpath(root, JSON_FOLDER)
                folder_url = relative_folder if relative_folder != "." else ""

                # Get frequency from frequency file
                frequency = get_frequency_from_file(freq_json_path)

                # Add main JSON entry
                if os.path.exists(main_json_path):
                    url = f"{RAW_BASE_URL}/{folder_url}/{folder_name}.json".strip("/")
                    lastmod = get_git_last_modified_date(main_json_path)
                    if not lastmod:
                        lastmod = datetime.now().strftime("%Y-%m-%d")
                    else:
                        lastmod = lastmod[:10]
                    sitemap_entries.append({
                        "url": url,
                        "lastmod": lastmod,
                        "changefreq": frequency
                    })

                # Add actions JSON entry if it exists
                if os.path.exists(actions_json_path):
                    url = f"{RAW_BASE_URL}/{folder_url}/{folder_name}_actions.json".strip("/")
                    lastmod = get_git_last_modified_date(actions_json_path)
                    if not lastmod:
                        lastmod = datetime.now().strftime("%Y-%m-%d")
                    else:
                        lastmod = lastmod[:10]
                    sitemap_entries.append({
                        "url": url,
                        "lastmod": lastmod,
                        "changefreq": frequency
                    })
                
    # Sort entries so oldest are first, newest are last
    sitemap_entries.sort(key=lambda x: x['lastmod'])
    
    # Generate the consolidated sitemap XML
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for entry in sitemap_entries:
        sitemap += "  <url>\n"
        sitemap += f"    <loc>{entry['url']}</loc>\n"
        sitemap += f"    <lastmod>{entry['lastmod']}</lastmod>\n"
        sitemap += f"    <changefreq>{entry['changefreq']}</changefreq>\n"
        sitemap += "  </url>\n"
    sitemap += "</urlset>"

    # Save sitemap to the root folder
    sitemap_file = "sitemap.xml"
    with open(sitemap_file, "w", encoding="utf-8") as f:
        f.write(sitemap)

    print(f"Sitemap generated successfully and saved as {sitemap_file}.")

if __name__ == "__main__":
    generate_sitemap()