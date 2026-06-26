import docker

client = docker.from_env()


def build_crash_report(event):
    container_id = event["container_id"]

    try:
        container = client.containers.get(container_id)

        logs = container.logs(tail=50).decode("utf-8")

        inspect = container.attrs
        state = inspect.get("State", {})

        return {
            "container_id": container_id,
            "name": inspect.get("Name", "").replace("/", ""),
            "reason": state.get("Error", "unknown"),
            "exit_code": state.get("ExitCode"),
            "oom_killed": state.get("OOMKilled", False),
            "logs_tail": logs,
            "timestamp": event["timestamp"]
        }

    except Exception as e:
        return {
            "container_id": container_id,
            "error": str(e),
            "timestamp": event["timestamp"]
        }