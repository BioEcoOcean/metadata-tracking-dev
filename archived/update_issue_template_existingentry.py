import os

def update_template_with_folders():
    folder_path = "jsonFiles"
    template_file = ".github/ISSUE_TEMPLATE/update_existing_entry.yml"

    # Get list of folder names within jsonFiles
    folder_names = [folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]

    # Format folder names into markdown list
    options = "\n".join([f"      - {folder}" for folder in folder_names])

    # Read the existing template
    with open(template_file, "r") as file:
        template_content = file.read()
    
    # Define the placeholder string where the folders should be inserted
    placeholder = "      - None (please submit a new issue instead)"
    # Find the placeholder in the template file
    options_section_start = template_content.find(placeholder) + len(placeholder)
    
    # If the placeholder is found, append the formatted folder names
    if options_section_start != -1:
        # Create the updated content by inserting the formatted folder names
        updated_template = (template_content[:options_section_start] + "\n" +
                            options + "\n" +
                            template_content[options_section_start:])
        # Write the updated template back to the file
        with open(template_file, 'w') as file:
            file.write(updated_template)
        print("Successfully updated the issue template.")
    else:
        print("Placeholder 'None' not found in the template. Please check the template format.")

if __name__ == "__main__":
    update_template_with_folders()
