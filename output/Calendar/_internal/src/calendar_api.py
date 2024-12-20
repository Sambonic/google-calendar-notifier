import datetime
import os.path
import sys
from typing import Optional, Tuple

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .paths import TOKEN, CREDENTIALS

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_tokens() -> str:
    """
    Get credentials
    """
    print("Getting new token!")
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
    print(f"Flow : {flow}")
    creds = flow.run_local_server(port=0)
    print(f"CREDS={creds}")
    # Save the tokens for the next run
    with open(TOKEN, "w") as token:
        token.write(creds.to_json())

    return creds 

def auth() -> str:
    """
    Authenticate Google Calendar API
    """
    creds = None
    try:
        if os.path.exists(TOKEN):
            print("Token path exists!")
            creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
            
        if not creds or not creds.valid:
            print("Token Expired")
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing expired credentials...")
                creds.refresh(Request())
            else:
                print("Getting new credentials...")
                creds = get_tokens()

            with open(TOKEN, "w") as token:
                token.write(creds.to_json())

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        creds = get_tokens()
        with open(TOKEN, "w") as token:
            token.write(creds.to_json())
    
    return creds

def events(title="Upcoming Events", desc="") -> Optional[Tuple[str, str]]:
    """
    Call Google Calendar API to gather the events.
    """
    try:
        service = build("calendar", "v3", credentials=auth())
        now = datetime.datetime.now().isoformat() + "Z"
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        if not events:
            print("No upcoming events found.")
            return

        seen_summaries = set()
        for event in events:
            summary = event.get('summary', 'No Title')
            if summary in seen_summaries:
                continue
            seen_summaries.add(summary)
            
            start = event["start"].get("dateTime", event["start"].get("date"))
            if start == datetime.date.today().isoformat():
                title = "Today's Events"
            
            try:
                event_desc = f"{start} | {summary} | {event.get('description', '')}"[:48] +"\n"
            except KeyError as error:
                event_desc = f"{start} | {summary} | "[:48] +"\n"
            desc += event_desc

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit()

    print("Successfully Gathered Events!")
    return title, desc
