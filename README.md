# DevOps Python Toolkit

A collection of practical Python utilities for DevOps automation.

Each folder contains a standalone tool with source code, tests, sample input, and notes where useful.

## Tools

### Log Parser

Location: `log-parser/`

A CLI tool that analyzes web access logs.

Features:

- Top IP address counts
- Top HTTP status code counts
- Failed request filtering
- Most requested endpoints
- `--limit` support
- JSON output
- Clean error handling with `stderr`
- Pytest coverage for parser functions and CLI behavior

Run:

```bash
cd log-parser
python3 parser.py sample_access.log --top-ips --limit 3
```

Run tests from the repo root:

```bash
python3 -m pytest
```

If using the virtual environment from the parent workspace:

```bash
../.venv/bin/python -m pytest
```
