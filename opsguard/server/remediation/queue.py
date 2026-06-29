from collections import deque
from threading import Lock

execution_queue = deque()
queue_lock = Lock()


def push_job(job):
    with queue_lock:
        execution_queue.append(job)


def pop_job():
    with queue_lock:
        if execution_queue:
            return execution_queue.popleft()
    return None