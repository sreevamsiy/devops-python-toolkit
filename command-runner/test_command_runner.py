import json
import subprocess
import sys
from pathlib import Path

from command_runner import run_command

TOOL_DIR = Path(__file__).parent

def test_run_command_success():
    result = run_command("echo hello", 5)

    assert result["success"] is True
    assert result["stdout"] == "hello"
    assert result["stderr"] == ""
    assert result["returncode"] == 0

def test_run_command_failure():
    result = run_command("ls missing-file", 5)

    assert result["success"] is False
    assert result["returncode"] != 0
    assert "missing-file" in result["stderr"]

def test_run_command_timeout():
    result = run_command("sleep 5", 1)

    assert result["success"] is False
    assert result["stderr"] == "Error: command timed out after 1 seconds"
    assert result["returncode"] == 124

def test_cli_success():
    result = subprocess.run(
        [sys.executable, "command_runner.py", "echo hello"],
        capture_output=True,
        text=True,
        cwd=TOOL_DIR,
    )

    assert result.stderr == ""
    assert result.stdout.strip() == "hello"
    assert result.returncode == 0

def test_cli_failure():
    result = subprocess.run(
        [sys.executable, "command_runner.py", "ls missing-file"],
        capture_output=True,
        text=True,
        cwd=TOOL_DIR,
    )

    assert result.returncode != 0
    assert "missing-file" in result.stderr

def test_cli_rejects_invalid_timeout():
    result = subprocess.run(
        [sys.executable, "command_runner.py", "echo hello", "--timeout", "0"],
        capture_output=True,
        text=True,
        cwd=TOOL_DIR,
    )

    assert result.returncode == 1
    assert "Error: --timeout must be greater than 0" in result.stderr

def test_cli_timeout():
    result = subprocess.run(
        [sys.executable, "command_runner.py", "sleep 5", "--timeout", "1"],
        capture_output=True,
        text=True,
        cwd=TOOL_DIR,
    )

    assert result.returncode == 124
    assert "Error: command timed out after 1 seconds" in result.stderr

def test_cli_json_success():
    result = subprocess.run(
        [sys.executable, "command_runner.py", "echo hello", "--json"],
        capture_output=True,
        text=True,
        cwd=TOOL_DIR,
    )

    data = json.loads(result.stdout)

    assert result.returncode == 0
    assert data["success"] is True
    assert data["stdout"] == "hello"
    assert data["stderr"] == ""
    assert data["returncode"] == 0
    assert result.stderr == ""

def test_cli_json_failure():
    result = subprocess.run(
        [sys.executable, "command_runner.py", "ls missing-file", "--json"],
        capture_output=True,
        text=True,
        cwd=TOOL_DIR,
    )

    data = json.loads(result.stdout)

    assert result.returncode == 1
    assert data["success"] is False
    assert data["stdout"] == ""
    assert "missing-file" in data["stderr"]
    assert data["returncode"] == 1
    assert result.stderr == ""