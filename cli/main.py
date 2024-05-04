import os
import subprocess
import anthropic
from claude import create_prompt, parse_create_result
from reader.read_dir import get_files_content

def create_project_folder():
    project_name = "example"
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)

def create_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)

def initialize_webapp(prompt):
    project_description = prompt
    prompt = create_prompt(project_description)
    result = send_prompt(prompt)
    file_structure = parse_create_result(result)
    
    if file_structure:
        for filename, content in file_structure.items():
            create_file(filename, content)
        print("Web app initialized successfully.")
    else:
        print("Failed to initialize the web app.")

def start_webapp():
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

def handle_request(request):
    files_content = get_files_content("example")
    prompt = f"""
The current state of the project is as follows:

{files_content}

The user has made the following request:

{request}

Return the result in the following JSON format ONLY, without any explanations or additional text:
{{
    "files": [
        {{
            "name": "index.html",
            "content": "<file_content>"
        }},
        {{
            "name": "styles.css",
            "content": "<file_content>"
        }},
        {{
            "name": "script.js",
            "content": "<file_content>"
        }}
    ]
}}
"""
    result = send_prompt(prompt)
    file_structure = parse_create_result(result)
    
    if file_structure:
        for filename, content in file_structure.items():
            create_file(filename, content)
        print("Project updated successfully.")
    else:
        print("Failed to update the project.")

def main():
    create_project_folder()
    
    while True:
        prompt = input("Enter a command (create <project_description>, request <request>, restart, or quit): ")
        
        if prompt.startswith("create "):
            project_description = prompt[7:]  # Extract the project description
            initialize_webapp(project_description)
            start_webapp()
        elif prompt.startswith("request "):
            request = prompt[8:]  # Extract the request
            handle_request(request)
            start_webapp()
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