import argparse
import multiprocessing as mp

from multiprocessing import Queue
from utils import (
    generate_notifications,
    check_new_events,
)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('time_before_event_min', type=int, default=1, help='Time before event in minutes for the notification.')
    args = parser.parse_args()

    q = Queue()
    jobs_to_do = []
    p1 = mp.Process(target=check_new_events, args=(q, jobs_to_do,))
    p1.start()
    p2 = mp.Process(target=generate_notifications, args=(q, args.time_before_event_min, ))
    p2.start()
    p1.join()
    p2.join()

if __name__=='__main__':
    main()