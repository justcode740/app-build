import os
import json
def get_files_content(folder_path):
    file_contents = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_contents[relative_path] = content
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    # Convert dictionary to JSON string
    json_content = json.dumps(file_contents)
    print(json_content)
    return json_content

if __name__ == "__main__":
    get_files_content("../example")