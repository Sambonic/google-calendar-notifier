from plyer import notification
from .calendar_api import events
from .paths import ICON

def notify() -> None:
    """
    Create the notification.
    """
    try:
        title, desc = events()
        print(f"Title: {title}, Description: {desc}")
        
        # Create notification and define character limits to title and message
        notification.notify(
            title=title[:64],
            message=desc[:256],
            app_name="Calendar",
            app_icon=ICON,
            timeout=None)
        
        print("Notification displayed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Exiting script")


