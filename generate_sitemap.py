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
    
def generate_sitemap():
    """Generates a single sitemap for all .json files in the jsonFiles folder and its subfolders."""
    sitemap_entries = []

    # Traverse all subfolders and gather .json file data
    for root, dirs, files in os.walk(JSON_FOLDER):
        print(f"Checking folder: {root}")
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                print(f"  Found JSON file: {file_path}")
                relative_folder = os.path.relpath(root, JSON_FOLDER)
                folder_name = relative_folder if relative_folder != "." else ""
                
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    url = f"{RAW_BASE_URL}/{folder_name}/{file_name}".strip("/")
                    frequency = data.get("frequency", "never")
                    lastmod = get_git_last_modified_date(file_path)
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