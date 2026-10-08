# AgentMD Python Backend

Python backend for the AgentMd project, ported from the original Node.js/Express application.

## Features

- FastAPI REST API
- Session-based authentication
- Provider configuration management
- Model synchronization routes
- Chat endpoints compatible with the frontend
- RAG upload and file listing
- SQLite database for persistence and metadata

## Requirements

- Python 3.10+
- pip

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app:app --host 0.0.0.0 --port 1010 --reload
```

or:

```bash
python -m agentmd
```

## API

Main base URL:

```text
http://localhost:1010/api
```

Example endpoints:

- GET `/api/session`
- GET `/api/settings`
- GET `/api/models`
- POST `/api/chat/init`
- POST `/api/chat/compare/init`
- POST `/api/rag/files`
- GET `/api/rag/files`

## Notes

This repository is intended as a Python backend replacement for the original Node.js version. The frontend remains separate and should point to this backend at `http://localhost:1010/api`.
