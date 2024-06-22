from win10toast_persist import ToastNotifier
import sys
from .calendar_api import events
from .paths import ICON

def notify() -> None:
    title, desc = events()
    toaster = ToastNotifier()
    toaster.show_toast(
    title=title,
    msg=desc,
    icon_path=ICON,
    duration=None)
    sys.exit()
