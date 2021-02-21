import datetime
from calendar_notification.utils import get_events

events = get_events()

if not events:
    print('No upcoming events found.')
else:
    for event in events:
        print(event['start'])
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = start[:-6]
        print(start)
        time_to_event = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S') - datetime.datetime.now()
        print('Time to event:', time_to_event)