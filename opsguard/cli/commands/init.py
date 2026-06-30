from pathlib import Path
import json
import uuid


def init_project():
    project_root = Path.cwd()
    opsguard_dir = project_root / ".opsguard"

    opsguard_dir.mkdir(exist_ok=True)

    config_file = opsguard_dir / "config.json"

    config = {
        "project_id": str(uuid.uuid4()),
        "project_name": project_root.name,
        "project_path": str(project_root),
        "containers": []
    }

    config_file.write_text(json.dumps(config, indent=2))

    print("✅ OpsGuard initialized")
    print(f"Project: {config['project_name']}")