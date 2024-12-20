import os
import re
import sys
import json

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

    # Extract content between ``` markers in the issue body
    #match = re.search(r"```json(.*?)```", issue_body, re.DOTALL)
    issue_cleaned = re.sub(r"^### Metadata Submission[\r\n]*\`*json", "", issue_body)
    issue_cleaned = re.sub(r"\`*$", "", issue_cleaned)
    if not match:
        print("No content found between ``` markers in the issue body.")
        sys.exit(1)
    
    content = issue_cleaned.strip()
    print(f"Extracted Content: {content}")

    # Parse the JSON content
    try:
        json_content = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)

    # Write content to a JSON file in the folder
    json_file_name = f"{folder_name}.json"
    json_file_path = os.path.join(folder_path, json_file_name)
    with open(json_file_path, "w") as json_file:
        json.dump(json_content, json_file, indent=4)
    
    print(f"Metadata saved to {json_file_path}")


if __name__ == "__main__":
    # Expecting issue_title and issue_body as command-line arguments
    if len(sys.argv) != 3:
        print("Usage: process_issues.py <issue_title> <issue_body>")
        sys.exit(1)
    
    issue_title = sys.argv[1]
    issue_body = sys.argv[2]

    process_github_issue(issue_title, issue_body)
