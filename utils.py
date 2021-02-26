import datetime
import time
import requests
import os.path
import pickle
import platform
import threading

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from plyer import notification

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_events():
    """Returns the 10 next events on Google Calendar

    Returns:
        list: list of events
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events

def string_to_datetime(datetime_str):
    """Returns the datetime object representation of a given string.

    Args:
        datetime_str (string): String with the date and time.

    Returns:
        datetime: datetime object.
    """
    date_in_datetime_format = datetime.datetime.strptime(
        datetime_str[:-6],
        '%Y-%m-%dT%H:%M:%S'
    )
    return date_in_datetime_format

def get_event_info(event):
    """Returns start time and summary of the event.

    Args:
        event (dict): dictionary with event info.

    Returns:
        datetime, string : datetime object with start time of event and string with the summary 
    """
    start = event['start'].get('dateTime', event['start'].get('date'))
    summary = event['summary']
    return start, summary

def generate_notifications(q, time_before_event_min=1):
    """Creates a thread for an event notification.

    Args:
        q (Queue): Queue object with tasks
    """
    while True:
        if not q.empty():
            print('Preparing notification...')
            event = q.get()
            t = threading.Thread(target=notify, args=(event,time_before_event_min, ))
            t.start()

def notify(event, time_before_event_min=1):
    """Waits till the notification and then performs a push notification

    Args:
        q (Queue): Queue object with tasks
    """
    start, summary = get_event_info(event)

    time_to_notification = (string_to_datetime(start) 
        - datetime.datetime.now() 
        - datetime.timedelta(minutes=time_before_event_min)
    )
    
    if time_to_notification.total_seconds() > 0:
        time.sleep(time_to_notification.total_seconds())

        if platform.system=='Darwin':

            os.system("""
                    osascript -e 'display notification "{}" with title "{}"'
                    """.format(start, summary))
        else:

            notification.notify(
                title=summary,
                message=start,
                timeout=2
            )

def check_new_events(q, jobs_to_do):
    while True:
        events = get_events()

        for event in events:
            #if event not in q.queue:

            if event not in jobs_to_do:
                q.put(event)
                jobs_to_do.append(event)
    return