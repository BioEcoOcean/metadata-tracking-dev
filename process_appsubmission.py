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
    pattern = r"###\s*(Metadata Submission|Actions JSON|Metadata Frequency)\s*```json\s*({.*?})\s*```"
    matches = re.findall(pattern, issue_body, re.DOTALL)
    sections = {}
    for heading, json_text in matches:
        sections[heading.strip()] = json_text.strip()
    return sections

# Function to process the json content
def process_github_issue(issue_title, issue_body):
    # Extract the JSON from the markdown sections first
    sections = extract_sections(issue_body) 
    if "Metadata Submission" not in sections:
        print("No 'Metadata Submission' section found in issue body.")
        sys.exit(1)
    
    json_text = sections["Metadata Submission"]
    
    try:
        data = json.loads(json_text)
        print("Parsed JSON-LD:", data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON-LD: {e}")
        sys.exit(1)
    
    # Parse the issue body as JSON-LD
    try:
        data = json.loads(issue_body)
        print("Parsed JSON-LD:", data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON-LD: {e}")
        sys.exit(1)

    # Find the Project node in the @graph to determine folder name
    folder_base = None
    if "@graph" in data:
        for node in data["@graph"]:
            if node.get("@type") == "Project" or node.get("@type") == "schema:Project":
                folder_base = node.get("schema:name") or node.get("schema:legalName")
                break
    if not folder_base:
        print("No Project node with a name found in the @graph.")
        sys.exit(1)

    folder_name = re.sub(r"[^\w\-_]", "_", folder_base)
    folder_path = f"jsonFiles/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)
    # Debugging
    print("Folder name:", folder_name)
    print("Folder path:", folder_path)    
    print("issue body",issue_body)
    # Save the entire JSON-LD as a single file
    json_file_path = os.path.join(folder_path, f"{folder_name}.json")
    print(f"Saving JSON-LD to {json_file_path}")
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, cls=setEncoder)
    print(f"JSON-LD saved to {json_file_path}")

if __name__ == "__main__":
    # Expecting issue_title and issue_body as command-line arguments
    if len(sys.argv) != 3:
        print("Usage: process_issues.py <issue_title> <issue_body>")
        sys.exit(1)
    
    issue_title = sys.argv[1]
    issue_body = sys.argv[2]

    process_github_issue(issue_title, issue_body)
