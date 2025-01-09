import json
import os
from datetime import datetime

# Define constants
REPO_ORG = "BioEcoOcean"
REPO_NAME = "metadata-tracking-dev"
BRANCH = "refs/heads/main"  
JSON_FOLDER = "jsonFiles"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{REPO_ORG}/{REPO_NAME}/{BRANCH}/{JSON_FOLDER}"

def generate_sitemap():
    # Load all sitemap entries
    sitemap_entries = []
    # Iterate through subfolders in the JSON folder
    for root, dirs, files in os.walk(JSON_FOLDER):
        for file_name in files:
            if file_name.endswith(".json"):
                json_path = os.path.join(root, file_name)
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        # Extract URL and frequency from the JSON file
                        url = data.get("url", f"{RAW_BASE_URL}/{os.path.relpath(json_path, JSON_FOLDER)}")
                        frequency = data.get("frequency", "never")  # Default to 'weekly' if not specified
                        lastmod = datetime.now().strftime("%Y-%m-%d")  # Use current date as last modified

                        # Append the entry to the sitemap
                        sitemap_entries.append({
                            "url": url,
                            "lastmod": lastmod,
                            "changefreq": frequency
                        })
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {json_path}")
                except Exception as e:
                    print(f"Unexpected error with file {json_path}: {e}")

    # Generate sitemap XML
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for entry in sitemap_entries:
        sitemap += "  <url>\n"
        sitemap += f"    <loc>{entry['url']}</loc>\n"
        sitemap += f"    <lastmod>{entry['lastmod']}</lastmod>\n"
        sitemap += f"    <changefreq>{entry['changefreq']}</changefreq>\n"
        sitemap += "  </url>\n"
    sitemap += "</urlset>"

    # Save sitemap
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)

    print("Sitemap generated successfully.")

if __name__ == "__main__":
    generate_sitemap()
