import os
import re
import sys
import json
class setEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def process_github_issue(issue_title, issue_body):
    """
    Process a GitHub issue and create a folder with a JSON file based on its content.
    
    Args:
        issue_title (str): The title of the GitHub issue.
        issue_body (str): The body of the GitHub issue.
    """
    # Extract the 'name' from the issue title using regex
    match = re.match(r"^New Submission: (.+)$", issue_title)
    if not match:
        print("No valid 'name' found in the issue title.")
        sys.exit(1)
    
    name = match.group(1)
    print(f"Extracted Name: {name}")
    
    # Sanitize the folder name
    folder_name = re.sub(r"[^\w\-_]", "_", name)
    folder_path = f"jsonFiles/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)
    print(folder_name)
    print(folder_path)
    
    print("issue body",issue_body)

    # Clean the issue body content to extract JSON between ```json
    issue_cleaned = re.sub(r"(?s)^### Metadata Submission\s*```json", "", issue_body)
    issue_cleaned = re.sub(r"```$", "", issue_cleaned).strip()

    print(f"Cleaned Issue: {issue_cleaned}")

    # Try parsing the cleaned content as JSON
    try:
        json_content = json.loads(issue_cleaned)
        print("Parsed JSON successfully:", json_content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)

    # Write content to a JSON file in the folder
    json_file_name = f"{folder_name}.json"
    json_file_path = os.path.join(folder_path, json_file_name)
    print("json path", json_file_path)
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_content, json_file, indent=4, cls=setEncoder)
    
    print(f"Metadata saved to {json_file_path}")

if __name__ == "__main__":
    # Expecting issue_title and issue_body as command-line arguments
    if len(sys.argv) != 3:
        print("Usage: process_issues.py <issue_title> <issue_body>")
        sys.exit(1)
    
    issue_title = sys.argv[1]
    issue_body = sys.argv[2]

    process_github_issue(issue_title, issue_body)
