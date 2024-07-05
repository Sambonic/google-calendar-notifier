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
  flow = InstalledAppFlow.from_client_secrets_file(
      CREDENTIALS, SCOPES
  )
  print(f"Flow : {flow}")
  creds = flow.run_local_server(port=0)
  print(f"CREDS={creds}")
  # Save the tokens for the next run
  with open(TOKEN, "w") as token:
    token.write(creds.to_json())
  return creds 

def auth() -> str:
  """
  Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  try:
    creds = None

    if os.path.exists(TOKEN):
      creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)

    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        creds = get_tokens()

  except Exception as e:
    print(f"An unexpected error occurred: {e}")
    creds = get_tokens()
    return creds
  return creds

def events(title = "Upcoming Events", desc = "")-> Optional[Tuple[str, str]]:
  try:
    service = build("calendar", "v3", credentials=auth())

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"
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

    title = "Upcoming Events"
    desc = ""
    for i, event in enumerate(events):
      start = event["start"].get("dateTime", event["start"].get("date"))
      if start == datetime.date.today():
        title = "Today's Events"
      try:
        event_desc = f"{start}, {event["summary"]}, {event["description"]}\n"
      except KeyError as error:
        event_desc = f"{start}, {event["summary"]}\n"
      desc += event_desc

  except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit()

  return title, desc