import datetime
import time
from threading import Thread
from plyer import notification

class Notifier(Thread):
    def __init__(self, queue):
        super.__init__(self)
        self.queue = queue

    def run(self, advance_notification_hours=1):
        while True:
            event = self.queue.get()
            self.queue.task.done()

            event_time             = 
            notification_time      = event_time - datetime.timedelta(hours=advance_notification_hours)
            now                    = datetime.datetime.now()

            if notification_time:
                exit()
            else:
                
                time.sleep((notification_time - now).total_seconds)

                notification.notify(
                    title =,
                    app_icon=None,
                    toast=False
                )

"""