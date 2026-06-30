from opsguard.cli.utils.container_registry import get_registered_containers
from opsguard.cli.utils.project import get_opsguard_dir
import json


def status():
    print("📊 OpsGuard Status")

    containers = get_registered_containers()

    print(f"\nRegistered containers: {len(containers)}")
    for c in containers:
        print(f" - {c['container_name']}")

    print("\nProject config:")
    config = json.loads((get_opsguard_dir() / "config.json").read_text())
    print(json.dumps(config, indent=2))