import subprocess
import time
import sys
import requests
from .paths import EXE

def check_internet_connection():
    """
    Checks if internet connection exists.
    Originally used ping command but that was inconsistent so there's that ig
    """
    try:
        response = requests.get("https://google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False    

def create_task() -> None:
    """
    Checks for the existence of the task and creates it if it doesn't exist.
    If the task exists, a message is printed and the script proceeds.
    """

    TASK_NAME = "CalendarNotificationSystem"
    
    # Command to check for task existence
    check_cmd = f'schtasks /Query /TN "{TASK_NAME}"'
    
    # Command to create task
    task_cmd = f'schtasks /create /SC ONLOGON /TN "CalendarNotificationSystem" /TR "{EXE}" /RL HIGHEST /F'

    try:
        # Retry logic for checking internet connection
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            if check_internet_connection():
                check_output = subprocess.run(check_cmd, capture_output=True, text=True)

                if check_output.returncode == 0:
                    print("Task already exists. Skipping creation")
                else:
                    subprocess.run(task_cmd, check=True)
                    print("Task created successfully!")
                break
            
            else:
                print(f"No internet connection. Retrying in 60 seconds... ({retry_count+1}/{max_retries})")
                time.sleep(60)
                retry_count += 1

        if retry_count == max_retries:
            print(f"Failed to launch task after {max_retries} retries.")
            sys.exit()

    except subprocess.CalledProcessError as e:
        print(f"Error checking or creating task: {e}")
