import json
from pathlib import Path
import subprocess
import sys

import pytest

from parser import parse_log_file, top_codes, top_ips, most_requested, failed_requests

EXERCISE_DIR = Path(__file__).parent
SAMPLE_LOG = EXERCISE_DIR / "sample_access.log"

@pytest.fixture
def records():
    return parse_log_file(SAMPLE_LOG)

def test_parse_log_file_skips_bad_lines(tmp_path):
    log_file = tmp_path / "test.log"

    log_file.write_text(
        '1.1.1.1 - - [23/May/2026:09:12:01 +0530] "GET /ok HTTP/1.1" 200 123 "-" "curl"\n'
        'bad malformed line\n'
        '2.2.2.2 - - [23/May/2026:09:12:02 +0530] "GET /bad HTTP/1.1" ERROR 456 "-" "curl"\n'
    )

    records = parse_log_file(log_file)

    assert len(records) == 1
    assert records[0]["ip"] == "1.1.1.1"
    assert records[0]["endpoint"] == "/ok"
    assert records[0]["http_code"] == 200
    assert records[0]["bytes"] == 123

def test_top_ips(records):
    assert top_ips(records, 1) == {"192.168.1.10": 5}

def test_top_codes(records):
    assert top_codes(records, 2) == {200: 16, 401: 2}

def test_failed_requests(records):
    failed = failed_requests(records)

    assert len(failed) == 7
    assert "401" in failed[0]

def test_most_requested(records):
    assert most_requested(records, 1) == {"/api/v1/users": 4}

def test_cli_rejects_invalid_limit():
    result = subprocess.run(
        [sys.executable, "parser.py", "sample_access.log", "--limit", "0"],
        capture_output=True,
        text=True,
        cwd=EXERCISE_DIR,
    )

    assert result.returncode == 1
    assert "Error: --limit must be greater than 0" in result.stderr

def test_cli_rejects_missing_file():
    result = subprocess.run(
        [sys.executable, "parser.py", "missing.log"],
        capture_output=True,
        text=True,
        cwd=EXERCISE_DIR,
    )

    assert result.returncode == 1
    assert "Error: file not found: missing.log" in result.stderr

def test_cli_top_ips_success():
    result = subprocess.run(
        [sys.executable, "parser.py", "sample_access.log", "--top-ips", "--limit", "1"],
        capture_output=True,
        text=True,
        cwd=EXERCISE_DIR,
    )

    assert result.returncode == 0
    assert "{'192.168.1.10': 5}" in result.stdout
    assert result.stderr == ""

def test_cli_json_top_ips_success():
    result = subprocess.run(
        [sys.executable, "parser.py", "sample_access.log", "--top-ips", "--limit", "1", "--json"],
        capture_output=True,
        text=True,
        cwd=EXERCISE_DIR,
    )

    data = json.loads(result.stdout)

    assert result.returncode == 0
    assert data == {"top_ips": {"192.168.1.10": 5}}
    assert result.stderr == ""
