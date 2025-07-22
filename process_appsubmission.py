import os
import re
import sys
import json
class setEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

# Function to handle the separate sections
def extract_sections(issue_body):
    # Split by headings, capturing heading and JSON
    pattern = r"(Metadata Submission|Actions JSON|Metadata Frequency)\s*({.*?})(?=(?:\n[A-Za-z ]+\n)|$)"
    matches = re.findall(pattern, issue_body, re.DOTALL)
    sections = {}
    for heading, json_text in matches:
        sections[heading.strip()] = json_text.strip()
    return sections

# Function to process the json content
def process_github_issue(issue_title, issue_body):
    # Extract the 'name' from the issue title using regex
    match = re.match(r"^New Submission: (.+)$", issue_title)
    if not match:
        print("No valid 'name' found in the issue title.")
        sys.exit(1)
    
    name = match.group(1)
    print(f"Extracted Name: {name}")
    
    # Extract JSON sections
    sections = extract_sections(issue_body)
    if "Metadata Submission" not in sections:
        print("No 'Metadata Submission' section found.")
        sys.exit(1)
    
    # Parse main metadata to get folder name
    try:
        main_json = json.loads(sections["Metadata Submission"])
        print("Parsed Metadata Submission:", main_json)
    except json.JSONDecodeError as e:
        print(f"Error decoding Metadata Submission JSON: {e}")
        sys.exit(1)

    # Sanitize the folder name
    folder_base = main_json.get("name") or main_json.get("legalName") or name
    folder_name = re.sub(r"[^\w\-_]", "_", folder_base)
    folder_path = f"jsonFiles/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)

    # Debugging
    print("Folder name:", folder_name)
    print("Folder path:", folder_path)    
    print("issue body",issue_body)

    # Save each section as its own JSON file
    filenames = {
        "Metadata Submission": f"{folder_name}.json",
        "Actions JSON": f"{folder_name}_actions.json",
        "Metadata Frequency": f"{folder_name}_frequency.json"
    }
    for heading, json_text in sections.items():
        try:
            content = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"Error decoding {heading} JSON: {e}")
            continue
        json_file_path = os.path.join(folder_path, filenames.get(heading, f"{folder_name}_{heading.lower().replace(' ', '_')}.json"))
        print(f"Saving {heading} to {json_file_path}")
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(content, json_file, indent=4, cls=setEncoder)
        print(f"{heading} saved to {json_file_path}")

if __name__ == "__main__":
    # Expecting issue_title and issue_body as command-line arguments
    if len(sys.argv) != 3:
        print("Usage: process_issues.py <issue_title> <issue_body>")
        sys.exit(1)
    
    issue_title = sys.argv[1]
    issue_body = sys.argv[2]

    process_github_issue(issue_title, issue_body)
