import os
import regex as re
import sys

def get_short_path(path: str) -> str:
    """
    Convert a long path with spaces to its short 8.3 path name.
    """
    pattern = r"\\([^\\]*\s[^\\]*)\\"
    matches = re.findall(pattern, path)

    if not matches:
        print("No matches found. Returning the original path.")
        return path
    
    output = path
    for match in re.findall(pattern, path):
        match_start = path.find(match)
        output = path[:match_start]
        try:
            shortened = os.popen(f'dir /x "{output}"').read()
            pattern_two = f"(<DIR>)(.*)({match})"
            match_two = re.search(pattern_two, shortened)
            
            if match_two:
                path = path.replace(match, match_two.group(2).strip())
                output = path

        except Exception as e:
            print(f"Exception occurred while converting path: {e}")
            return path  
    return output

def check_path_exists(path: str) -> str:
    """
    Check if the path exists.
    """
    if os.path.exists(path):
        print(f"Path verified and exists: {path}")
    else:
        print(f"Path does not exist: {path}")
    
    return path

"""
Identify parent directory and its subsequent children.
"""
parent_dir = os.path.dirname(os.path.dirname(__file__))
print(f"Parent directory: {parent_dir}")


ICON = check_path_exists(os.path.join(parent_dir, "images", "calendar.ico")).replace("\\", "/")
TOKEN = check_path_exists(os.path.join(parent_dir, "credentials", "token.json")).replace("\\", "/")
CREDENTIALS = check_path_exists(os.path.join(parent_dir, "credentials", "credentials.json")).replace("\\", "/")

# Handle path to Calendar.exe
if getattr(sys, 'frozen', False):
    exe_path = sys.executable
else:
    exe_path = check_path_exists(os.path.join(parent_dir, "output", "Calendar", "Calendar.exe"), is_file=True)

EXE = get_short_path(exe_path).replace("\\", "/")


print(f"Path to ICON: {ICON}")
print(f"Path to TOKEN: {TOKEN}")
print(f"Path to CREDENTIALS: {CREDENTIALS}")
print(f"Path to EXE (short path if applicable): {EXE}")
