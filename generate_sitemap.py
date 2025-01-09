import json
import os
from datetime import datetime

# Define constants
REPO_ORG = "BioEcoOcean"
REPO_NAME = "metadata-tracking-dev"
BRANCH = "refs/heads/main"  
JSON_FOLDER = "jsonFiles"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{REPO_ORG}/{REPO_NAME}/{BRANCH}/{JSON_FOLDER}"

def generate_sitemap_for_folder(folder_path, folder_name):
    """Generates a sitemap for a specific folder."""
    sitemap_entries = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                url = data.get("url", f"{RAW_BASE_URL}/{folder_name}/{file_name}")
                frequency = data.get("frequency", "never")
                lastmod = data.get("lastmod", datetime.utcnow().strftime("%Y-%m-%d"))
                sitemap_entries.append({
                    "url": url,
                    "lastmod": lastmod,
                    "changefreq": frequency
                })

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

    # Save sitemap to folder
    sitemap_file = os.path.join(folder_path, "sitemap.xml")
    with open(sitemap_file, "w", encoding="utf-8") as f:
        f.write(sitemap)

    print("Sitemap generated successfully.")

def generate_all_sitemaps():
    """Generates sitemaps for all folders in the JSON_FOLDER."""
    for folder_name in os.listdir(JSON_FOLDER):
        folder_path = os.path.join(JSON_FOLDER, folder_name)
        if os.path.isdir(folder_path):
            generate_sitemap_for_folder(folder_path, folder_name)

if __name__ == "__main__":
    generate_all_sitemaps()
