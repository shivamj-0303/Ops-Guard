# OpsGuard

> **AI-powered Runtime Incident Detection & Intelligent Auto-Remediation for Docker Workloads**

OpsGuard continuously monitors your Docker containers, detects runtime failures, investigates the root cause using AI, correlates failures with source code and Git history, generates an executable remediation plan, and allows engineers to safely approve and execute remediation actions.

---

## Features

- Real-time Docker container monitoring
- Automatic runtime incident detection
- Structured incident reports
- Log collection and stack trace analysis
- AI-powered root cause investigation
- Source code context collection
- Git commit correlation
- Dependency analysis
- AI-generated remediation plans
- Human approval workflow
- Tool-based remediation execution
- Complete execution history
- Safe execution through registered tools
- Simple Python package installation

---

# Architecture

```text
                    Docker Events
                          │
                          ▼
                 Crash Detection Engine
                          │
                          ▼
                  Incident Generation
                          │
                          ▼
                 Context Collection Layer
          ┌──────────┬──────────┬──────────┐
          │          │          │          │
      Docker      Source      Git     Dependencies
          │          │          │          │
          └──────────┴──────────┴──────────┘
                          │
                          ▼
                 AI Root Cause Analysis
                          │
                          ▼
               AI Execution Plan Generator
                          │
                          ▼
                 Approval Required
                          │
                          ▼
                  Tool Execution Engine
                          │
                          ▼
               Incident Successfully Resolved
```

---

# Installation

## Requirements

- Python 3.10+
- Docker
- Git
- Ollama (for local AI)
- Linux/macOS (Windows support coming soon)

---

## Install

```bash
pip install opsguard
```

Verify installation:

```bash
opsguard --help
```

---

# Quick Start

## 1. Navigate to your project

```bash
cd your-project
```

---

## 2. Initialize OpsGuard

```bash
opsguard init
```

This creates:

```
.opsguard/
└── config.json
```

---

## 3. Register your Docker container

```bash
opsguard register-container my-app
```

---

## 4. Start OpsGuard

```bash
opsguard start
```

OpsGuard will now continuously monitor registered containers.

---

# Workflow

```
Container Crash
      │
      ▼
Collect Logs
      │
      ▼
Analyze Stack Trace
      │
      ▼
Collect Source Code
      │
      ▼
Analyze Git History
      │
      ▼
Collect Dependencies
      │
      ▼
AI Investigation
      │
      ▼
Execution Plan
      │
      ▼
Human Approval
      │
      ▼
Execute Tools
      │
      ▼
Execution Report
```

---

# Example Incident Lifecycle

### Runtime Failure

```
NameError: name 'os' is not defined
```

↓

OpsGuard automatically:

- Collects logs
- Detects stack trace
- Locates affected source file
- Collects Git history
- Finds recent commits
- Builds investigation context
- Sends investigation to AI

↓

AI Investigation

```json
{
  "root_cause": "Missing import for os module.",
  "severity": "low",
  "confidence": 92
}
```

↓

Execution Plan

```json
{
  "status": "PENDING_APPROVAL",
  "actions": [
    {
      "tool": "filesystem.replace_text",
      "arguments": {
        "filename": "database.py"
      }
    },
    {
      "tool": "docker.restart_container"
    }
  ]
}
```

↓

Engineer approves

↓

OpsGuard executes the plan

↓

Execution report generated

---

# Project Structure

```
opsguard/
│
├── cli/
│
├── server/
│   ├── ai/
│   ├── analysis/
│   ├── context/
│   ├── execution/
│   ├── observer/
│   ├── remediation/
│   ├── storage/
│   └── tools/
│
└── memory/
```

---

# Supported AI Providers

Current

- Ollama

Planned

- OpenAI
- Anthropic Claude
- Google Gemini
- Azure OpenAI
- Local Llama.cpp

---

# Built-in Tools

Current tools include:

Docker

- Collect logs
- Restart container
- Inspect container
- List containers

Filesystem

- Read file
- Replace text
- Find file

More tools will be added in future releases.

---

# Safety

OpsGuard **never executes AI output directly.**

Every action must be converted into structured tool calls.

Example:

```json
{
    "tool": "filesystem.replace_text",
    "arguments": {}
}
```

instead of

```bash
rm -rf /
```

This design prevents arbitrary command execution.

---

# Roadmap

## v0.1

- Docker monitoring
- AI investigation
- Human approval
- Tool execution

## v0.2

- Better CLI
- Doctor command
- Better diagnostics

## v0.3

- Web Dashboard
- Live incidents
- Approval UI

## v0.4

- Kubernetes support

## v0.5

- Cloud deployments

## v1.0

- Production-ready platform

---

# Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Submit a Pull Request.

---

# License

This project is licensed under the MIT License.

See the LICENSE file for details.

---

# Author

**Shivam Jangid**

---

# Disclaimer

OpsGuard is currently under active development.

While remediation actions are executed only after explicit approval, always review generated execution plans before applying them to production environments.

---

# Star the Project 

If you find OpsGuard useful, consider starring the repository to support the project and stay updated with future releases.