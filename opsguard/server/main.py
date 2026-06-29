import os
import json
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from opsguard.server.tools.registry import execute_tool
import opsguard.server.tools.docker_tools
import opsguard.server.tools.filesystem_tools
from opsguard.server.observer.docker_events import stream_events
from opsguard.server.observer.crash_detector import build_crash_report
from opsguard.server.analysis.root_cause import analyze_crash
from opsguard.server.observer.incident_manager import (
    create_incident,
    get_incident,
    close_incident
)
from opsguard.server.remediation.worker import (
    run_worker
)
from opsguard.cli.utils.project import (
    get_project_path
)
from opsguard.server.remediation.approvals import (
    APPROVALS_DIR
)
from opsguard.server.remediation.executor import (
    execute_remediation_plan
)
from opsguard.server.ai.execution_planner import (
    build_execution_plan
)
from opsguard.server.ai.investigator import (
    investigate_incident
)
from opsguard.server.analysis.evidence_collector import (
    collect_evidence
)

from opsguard.server.git_tools.commit_analyzer import (
    analyze_commit_relevance
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
from opsguard.server.remediation.planner import (
    build_remediation_plan
)
from opsguard.server.remediation.approvals import (
    save_approval_request
)
from opsguard.server.context.collector import (
    collect_context
)
from opsguard.cli.utils.project import get_opsguard_dir

from opsguard.server.git_tools.git_correlator import get_recent_commits
from opsguard.server.analysis.trace_analyzer import analyze_trace
from contextlib import asynccontextmanager
import threading

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.environ.get("OPSGUARD_OBSERVER") == "1":
        start_observer()
    
    start_worker()

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
        "arguments": req.payload,
        "result": result
    }

@app.get("/commits")
def commits():
    return get_recent_commits()

@app.get("/approvals")
def approvals():
    approvals = []

    for file in APPROVALS_DIR.glob("*.json"):
        with open(file) as f:
            approvals.append(
                json.load(f)
            )

    return approvals

@app.post("/approvals/{incident_id}/approve")
def approve(incident_id: str):

    approval_file = (
        get_opsguard_dir()
        / "approvals"
        / f"{incident_id}.json"
    )

    if not approval_file.exists():
        return {
            "status": "error",
            "message": "Approval file not found"
        }

    plan = json.loads(approval_file.read_text())

    # STEP 1: mark approved
    plan["status"] = "APPROVED"
    approval_file.write_text(json.dumps(plan, indent=2))

    # STEP 2: EXECUTE
    execution_result = execute_remediation_plan(
        incident_id,
        plan
    )

    return {
        "status": "approved_and_executed",
        "incident_id": incident_id,
        "execution": execution_result
    }


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
        report["name"],
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

    repo_path = get_project_path()
    print(repo_path)
    investigation_context = collect_context(
        report,
        trace_info,
        repo_path
    )
    provider = OllamaProvider()

    evidence = collect_evidence(
        report,
        analysis,
        trace_info
    )

    commit_analysis = analyze_commit_relevance(
        trace_info,
        recent_commits
    )
    investigation = investigate_incident(
        provider,
        report,
        analysis,
        investigation_context,
        recent_commits,
        evidence,
        commit_analysis
    )

    plan = build_execution_plan(
        provider,
        investigation,
        container_name,
        repo_path
    )

    approval_file = save_approval_request(
        incident["incident_id"],
        plan
    )
    print("STEP 4: Ollama Returned")
    print(investigation)
    
    final_report = {
        **incident,
        "analysis": analysis,
        "trace": trace_info,
        "docker": investigation_context.docker,
        "git": investigation_context.git,
        "source": investigation_context.source,
        "dependencies": investigation_context.dependencies,
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

def start_worker():
    t = threading.Thread(
        target=run_worker,
        daemon=True
    )
    t.start()