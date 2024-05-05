import os
import subprocess
import anthropic
from datetime import datetime
from claude import create_prompt, parse_create_result
from reader.read_dir import get_files_content

EXAMPLES_DIR = "/home/zw/apps/app-builder/examples"

def create_project_folder(project_name):
    project_path = os.path.join(EXAMPLES_DIR, project_name)
    os.makedirs(project_path, exist_ok=True)
    os.makedirs(os.path.join(project_path, "public"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "public", "css"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "public", "js"), exist_ok=True)
    return project_path

def create_file(project_path, filename, content):
    file_path = os.path.join(project_path, filename)
    with open(file_path, "w") as file:
        file.write(content)

def initialize_webapp(project_path, prompt):
    project_description = prompt
    prompt = create_prompt(project_description)
    result = send_prompt(prompt)
    file_structure = parse_create_result(result)
    
    if file_structure:
        for filename, content in file_structure.items():
            create_file(project_path, filename, content)
        print("Web app initialized successfully.")
    else:
        print("Failed to initialize the web app.")

def start_webapp(project_path):
    os.chdir(project_path)
    command = "npm start"
    subprocess.run(command.split())

def send_prompt(msg):
    api_key = os.getenv("CLAUDE_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2000,
        temperature=0.0,
        messages=[
            {"role": "user", "content": msg}
        ]
    )
    return message.content

def handle_request(project_name, request):
    project_path = os.path.join(EXAMPLES_DIR, project_name)
    files_content = get_files_content(project_path)
    prompt = f"""
The current state of the project is as follows:

{files_content}

The user has made the following request:

{request}

Return the result in the following JSON format ONLY, without any explanations or additional text:
{{
    "files": [
        {{
            "name": "public/index.html",
            "content": "<file_content>"
        }},
        {{
            "name": "public/css/style.css",
            "content": "<file_content>"
        }},
        {{
            "name": "public/js/app.js",
            "content": "<file_content>"
        }},
        {{
            "name": "server.js",
            "content": "<file_content>"
        }},
        {{
            "name": "package.json",
            "content": "<file_content>"
        }}
    ]
}}
"""
    result = send_prompt(prompt)
    file_structure = parse_create_result(result)
    
    if file_structure:
        for filename, content in file_structure.items():
            create_file(project_path, filename, content)
        print("Project updated successfully.")
    else:
        print("Failed to update the project.")

def main():
    while True:
        prompt = input("Enter a command (create <project_name> <project_description>, request <project_name> <request>, restart, or quit): ")
        
        if prompt.startswith("create "):
            command_parts = prompt.split(" ", 2)
            if len(command_parts) == 3:
                project_name = command_parts[1]
                project_description = command_parts[2]
                project_path = create_project_folder(project_name)
                initialize_webapp(project_path, project_description)
                start_webapp(project_path)
            else:
                print("Invalid create command. Usage: create <project_name> <project_description>")
        elif prompt.startswith("request "):
            command_parts = prompt.split(" ", 2)
            if len(command_parts) == 3:
                project_name = command_parts[1]
                request = command_parts[2]
                handle_request(project_name, request)
                start_webapp(os.path.join(EXAMPLES_DIR, project_name))
            else:
                print("Invalid request command. Usage: request <project_name> <request>")
        elif prompt.lower() == "restart":
            print("Restarting the CLI...")
            break
        elif prompt.lower() == "quit":
            print("Exiting the CLI.")
            return
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    while True:
        main()