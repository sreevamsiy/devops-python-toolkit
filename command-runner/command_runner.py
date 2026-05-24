import argparse
import json
import subprocess
import sys

def run_command(command, timeout):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Error: command timed out after {timeout} seconds",
            "returncode": 124
        }

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "returncode": result.returncode
    }

def main():
    parser = argparse.ArgumentParser(description="Run shell commands with timeout handling")
    parser.add_argument("command", help="Command to run")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout in seconds")
    parser.add_argument("--json", action="store_true", help="Print output in JSON")

    args = parser.parse_args()

    if args.timeout <= 0:
        print("Error: --timeout must be greater than 0", file=sys.stderr)
        sys.exit(1)

    result = run_command(args.command, args.timeout)

    if args.json:
        print(json.dumps(result, indent=2))
        sys.exit(result["returncode"])
    
    if result["success"]:
        if result["stdout"]:
            print(result["stdout"])
        sys.exit(0)

    if result["stderr"]:
        print(result["stderr"], file=sys.stderr)
    else:
        print(f"Error: command failed with exit code {result['returncode']}", file=sys.stderr)

    sys.exit(result['returncode'])
    
if __name__ == "__main__":
    main()