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

### Command Runner

Location: `command-runner/`

A CLI tool that runs shell commands with timeout handling and structured output.

Features:

- Runs shell commands with `subprocess`
- Captures `stdout`, `stderr`, and return code
- Timeout handling with exit code `124`
- Input validation for `--timeout`
- JSON output
- Clean error handling with `stderr`
- Pytest coverage for function behavior and CLI behavior

Run:

```bash
cd command-runner
python3 command_runner.py "echo hello"
python3 command_runner.py "sleep 5" --timeout 1
python3 command_runner.py "ls missing-file" --json
```

Run tests from the repo root:

```bash
python3 -m pytest
```

If using the virtual environment from the parent workspace:

```bash
../.venv/bin/python -m pytest
```
