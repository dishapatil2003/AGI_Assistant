import pyautogui
import time
import shutil
import os
import subprocess
import json

# Function to open an application (e.g., Notepad)
def open_application(app_name):
    print(f"Opening {app_name}...")
    if app_name == "notepad":
        subprocess.Popen(["notepad"])
    time.sleep(1)

# Function to type text into the application
def type_text(text):
    print(f"Typing text: {text}")
    pyautogui.write(text)
    pyautogui.press('enter')
    time.sleep(1)

# Function to save the file to D:\
def save_file():
    print("Saving file...")
    file_path = "D:\\daily_report.txt"
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)
    pyautogui.write(file_path)  # Provide full path
    pyautogui.press('enter')
    time.sleep(1)

    if os.path.exists(file_path):
        print(f"File saved successfully at {file_path}")
    else:
        print(f"File not found at {file_path}")

# Function to rename the file
def rename_file(old_name, new_name):
    print(f"Renaming file from {old_name} to {new_name}...")
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        print(f"File renamed to {new_name}")
    else:
        print(f"File not found at {old_name}")

# Function to move the file
def move_file(source_path, destination_path):
    print(f"Moving file from {source_path} to {destination_path}...")
    if os.path.exists(source_path):
        if not os.path.exists(os.path.dirname(destination_path)):
            os.makedirs(os.path.dirname(destination_path))
        shutil.move(source_path, destination_path)
        print(f"File moved successfully to {destination_path}")
    else:
        print(f"Source file not found at {source_path}")

# Execute each action based on the workflow steps
def execute_action(action):
    print(f"Executing action: {action['action']}")
    details = action.get('details', {})

    if action['action'] == 'open_app':
        open_application(details.get('app'))
    elif action['action'] == 'type_text':
        type_text(details.get('text'))
    elif action['action'] == 'save_file':
        save_file()
    elif action['action'] == 'rename_file':
        rename_file(details.get('old_name'), details.get('new_name'))
    elif action['action'] == 'move_file':
        move_file(details.get('source_path'), details.get('destination_path'))

    print("Workflow executed successfully!")

# Execute the full workflow from understood_actions.json
def execute_workflow():
    with open("data/understood_actions.json", "r") as f:
        actions = json.load(f)
    for action in actions['steps']:
        execute_action(action)

if __name__ == "__main__":
    execute_workflow()
