import os
import uvicorn


def start_opsguard():
    os.environ["OPSGUARD_OBSERVER"] = "1"

    uvicorn.run(
        "opsguard.server.main:app",
        host="0.0.0.0",
        port=8080
    )