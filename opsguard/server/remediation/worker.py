import time
from opsguard.server.remediation.queue import pop_job
from opsguard.server.remediation.executor import execute_remediation_plan
from opsguard.server.remediation.verifier import verify_container
from opsguard.server.core.incident_state import IncidentStatus


def run_worker():
    print("🚀 Execution Worker Started")

    while True:
        job = pop_job()

        if not job:
            time.sleep(2)
            continue

        incident_id = job["incident_id"]
        container_name = job["container_name"]

        print(f"⚙️ Executing {incident_id}")

        try:
            # STEP 1: EXECUTE
            result = execute_remediation_plan(
                incident_id,
                job
            )

            # STEP 2: VERIFY
            verification = verify_container(container_name)

            print("✔ Execution Result:", result)
            print("✔ Verification:", verification)

        except Exception as e:
            print("❌ Execution Failed:", str(e))