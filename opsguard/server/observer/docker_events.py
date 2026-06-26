import docker
from datetime import datetime
import time

client = docker.from_env()

# simple in-memory dedup store
recent_events = {}  # container_id -> timestamp


DEDUP_WINDOW_SECONDS = 5


def is_duplicate(container_id):
    now = time.time()

    if container_id in recent_events:
        if now - recent_events[container_id] < DEDUP_WINDOW_SECONDS:
            return True

    recent_events[container_id] = now
    return False


def stream_events(callback):

    for event in client.events(decode=True):
        try:
            if event.get("Type") != "container":
                continue

            action = event.get("Action")
            actor = event.get("Actor", {})
            container_id = actor.get("ID")

            if not container_id:
                continue

            # ONLY treat final death event
            if action != "die":
                continue

            # deduplicate
            if is_duplicate(container_id):
                continue

            payload = {
                "container_id": container_id[:12],
                "action": action,
                "timestamp": datetime.utcnow().isoformat(),
                "attributes": actor.get("Attributes", {})
            }

            callback(payload)

        except Exception as e:
            print("Event error:", str(e))