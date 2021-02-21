import datetime
import time
import os
import threading
import platform
import multiprocessing as mp

from multiprocessing import Queue
from calendar_notification.utils import get_events

ICON = '/Users/tiago/Projects/desktop_notifier/desktop_notification.py'

def string_to_datetime(datetime_str):
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
        start, summary : [description]
    """
    start = event['start'].get('dateTime', event['start'].get('date'))
    summary = event['summary']
    return start, summary

def generate_notifications(q):
    """[summary]

    Args:
        q ([type]): [description]
    """
    while True:
        if not q.empty():
            print('Preparing notification...')
            event = q.get()
            t = threading.Thread(target=notify, args=(event,))
            t.start()

        #else:
            #print('Nothing to notify.')

def notify(event, notification_before_event_hours=1):
    start, summary = get_event_info(event)
    time_to_notification = string_to_datetime(start) - datetime.datetime.now() - datetime.timedelta(minutes=1)


    time.sleep(time_to_notification.total_seconds())

    os.system("""
            osascript -e 'display notification "{}" with title "{}" with icon POSIX file "{}"'
            """.format(start, summary, ICON))


def check_new_events(q, jobs_to_do):
    while True:
        events = get_events()

        for event in events:
            #if event not in q.queue:

            if event not in jobs_to_do:
                q.put(event)
                jobs_to_do.append(event)
    return
            

def main():

    q = Queue()
    jobs_to_do = []
    p1 = mp.Process(target=check_new_events, args=(q, jobs_to_do,))
    p1.start()
    p2 = mp.Process(target=generate_notifications, args=(q,))
    p2.start()
    p1.join()
    p2.join()

if __name__=='__main__':
    main()