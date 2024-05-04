import anthropic
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

def create_prompt(project_description):
    print(project_description)
    prompt = f"""
Please generate the necessary files and code for a web app based on the following project description:

{project_description}

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

Make sure to include all the required files such as HTML, CSS, and JavaScript. Provide the complete code for each file.
"""
    return prompt

def parse_create_result(result):
    print(result)
    try:
        if isinstance(result, list):
            result = result[0].text  # Extract the text from the first element if result is a list
        data = json.loads(result)
        files = data.get("files", [])
        file_structure = {}
        for file in files:
            filename = file.get("name")
            content = file.get("content")
            if filename and content:
                file_structure[filename] = content
        return file_structure
    except (json.JSONDecodeError, AttributeError):
        print("Error: Invalid JSON format")
        return None, ""

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