import os

from fastapi import FastAPI
from pydantic import BaseModel
from opsguard.server.tools.registry import execute_tool
import opsguard.server.tools.docker_tools
from opsguard.server.observer.docker_events import stream_events
from opsguard.server.observer.crash_detector import build_crash_report
from opsguard.server.analysis.root_cause import analyze_crash
from opsguard.server.observer.incident_manager import (
    create_incident,
    get_incident,
    close_incident
)
from opsguard.server.ai.investigator import (
    investigate_incident
)

from opsguard.server.ai.mock_provider import (
    MockProvider
)
from opsguard.server.registry.repo_registry import (
    register_repo,
    list_repos
)
from opsguard.server.storage.incident_store import (
    save_incident
)
from opsguard.cli.utils.container_registry import (
    is_registered_container
)
from opsguard.server.storage.log_storage import (
    save_logs
)
from opsguard.server.ai.providers.ollama_provider import (
    OllamaProvider
)
from opsguard.server.git_tools.git_correlator import get_recent_commits
from opsguard.server.analysis.trace_analyzer import analyze_trace
from contextlib import asynccontextmanager
import threading

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.environ.get("OPSGUARD_OBSERVER") == "1":
        start_observer()

    yield

app = FastAPI(lifespan=lifespan)

class ToolRequest(BaseModel):
    tool_name: str
    payload: dict = {}

class RegisterRepoRequest(BaseModel):
    repo_id: str
    repo_path: str

@app.post("/repos/register")
def register_repository(
    req: RegisterRepoRequest
):
    register_repo(
        req.repo_id,
        req.repo_path
    )

    return {
        "status": "registered"
    }

@app.get("/repos")
def repos():
    return list_repos()

@app.get("/health")
def health():
    return {"status": "opsguard alive"}


@app.get("/tools")
def list_tools():
    from opsguard.server.tools.registry import TOOL_REGISTRY

    return {
        name: {
            "description": tool.description
        }
        for name, tool in TOOL_REGISTRY.items()
    }


@app.post("/execute")
def run_tool(req: ToolRequest):
    result = execute_tool(req.tool_name, req.payload)
    return {
        "tool": req.tool_name,
        "result": result
    }

@app.get("/commits")
def commits():
    return get_recent_commits()

def handle_event(event):
    print(
        "EVENT RECEIVED",
        threading.get_ident(),
        event["container_id"],
        event["action"]
    )
    report = build_crash_report(event)
    container_name = report["name"]

    if not is_registered_container(
        container_name
    ):
        print(
            f"Skipping unregistered container: {container_name}"
        )
        return
    incident = create_incident(
        report["container_id"],
        report["name"]
    )
    if not incident:
        return
    log_file = save_logs(
        incident["incident_id"],
        report["logs_tail"]
    )
    analysis = analyze_crash(report)

    trace_info = analyze_trace(
        report.get("logs_tail", "")
    )
    recent_commits = get_recent_commits(limit=3)
    provider = OllamaProvider()

    investigation = investigate_incident(
        provider,
        report,
        analysis,
        trace_info,
        recent_commits
    )
    print("STEP 4: Ollama Returned")
    print(investigation)

    final_report = {
        **incident,
        "analysis": analysis,
        "trace": trace_info,
        "recent_commits": recent_commits,
        "investigation": investigation,
        "log_file": log_file
    }
    save_incident(final_report)
    print("\n🚨 OPSGUARD INCIDENT REPORT")
    print(final_report)
    close_incident(report["container_id"])


def start_observer():
    thread = threading.Thread(
        target=stream_events,
        args=(handle_event,),
        daemon=True
    )
    thread.start()