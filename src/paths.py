import os
import regex as re

def get_short_path(path:str)->str:
    pattern = r"\\([^\\]*\s[^\\]*)\\"
    output = path
    for match in re.findall(pattern, path):
        match_start = path.find(match)
        output = path[:match_start]
        try:
            shortened = os.popen(f'dir /x "{output}"').read()

            pattern_two = f"(<DIR>)(.*)({match})"
            match_two = re.search(pattern_two,shortened)

            path = path.replace(match,match_two.group(2).strip())
            output = path
        except Exception:
            return path  
    return output

script_dir = os.path.dirname(os.path.dirname(__file__))

icon_path = os.path.join(script_dir, "images", "calendar.ico")
token_path = os.path.join(script_dir, "credentials", "token.json")
credentials_path = os.path.join(script_dir, "credentials", "credentials.json")
exe_path = os.path.join(os.path.dirname(script_dir), "Calendar.exe")

ICON = icon_path
TOKEN = token_path
CREDENTIALS = credentials_path
EXE = get_short_path(exe_path)

print(f"Path: {ICON}")
print(f"Path: {TOKEN}")
print(f"Path: {CREDENTIALS}")
print(f"Path: {EXE}")