def build_remediation_plan(investigation, container_name):
    print("INVESTIGATION")
    print(investigation)

    actions = []

    for step in investigation.get("repair_steps", []):
        print("Processing:", step)

        action_text = step["action"].lower()

        if "restart" in action_text:
            actions.append({
                "type": "RESTART_CONTAINER",
                "container_name": container_name
            })

    print("Generated actions:", actions)

    return {
        "status": "PENDING_APPROVAL",
        "actions": actions
    }