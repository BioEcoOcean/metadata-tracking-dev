import os
import json
import csv

# Path to the input JSON file and output CSV file
JSON_FOLDER = 'jsonFiles'
CSV_FILE = 'data/bioeco_list.csv'

rows = []

# Traverse all subfolders and find main JSON files
for root, dirs, files in os.walk(JSON_FOLDER):
    for file_name in files:
        if file_name.endswith('.json') and not file_name.endswith('_actions.json') and not file_name.endswith('_frequency.json'):
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    name = data.get('name', '')
                    shortname = data.get('legalName', '')
                    url = data.get('url', '')
                    rows.append([name, shortname, url])
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

# Write to CSV
with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Project Name', 'Short Name', 'URL'])
    writer.writerows(rows)

print(f"CSV file '{CSV_FILE}' created successfully.")
