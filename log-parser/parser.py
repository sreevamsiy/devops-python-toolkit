import argparse
import json
import sys

from collections import Counter

def parse_log_file(filename):
    line_list = []
    with open(filename, 'r') as file:
        for line in file:
            line_dict = {}
            parts = line.split()
            if len(parts) < 10:
                continue
            line_dict['ip'] = parts[0]
            line_dict['endpoint'] = parts[6]
            try:
                line_dict['http_code'] = int(parts[8])
                line_dict['bytes'] = int(parts[9])
            except ValueError:
                continue
            line_dict['raw'] = line.strip()
            line_list.append(line_dict)
    return line_list

def top_ips(records, limit):
    ip_count = Counter()

    for item in records:
        ip = item['ip']
        ip_count[ip] += 1

    return dict(ip_count.most_common(limit))

def top_codes(records, limit):
    code_counter = Counter()
    for item in records:
        code = item['http_code']
        code_counter[code] += 1

    return dict(code_counter.most_common(limit))

def failed_requests(records):
    failed_reqs = []
    for item in records:
        if item['http_code'] > 399:
            failed_reqs.append(item['raw'])
    return failed_reqs

def most_requested(records, limit):
    endpoint_counter = Counter()
    for item in records:
        ep = item['endpoint']
        endpoint_counter[ep] += 1

    return dict(endpoint_counter.most_common(limit))

def main():
    parser = argparse.ArgumentParser(description='Analyze web access logs')
    parser.add_argument("filename", help="Path to access log file")
    parser.add_argument("--top-ips", action="store_true", help="Show top IP addresses")
    parser.add_argument("--top-codes", action="store_true", help="Show top HTTP status codes")
    parser.add_argument("--failed", action="store_true", help="Show failed requests")
    parser.add_argument("--top-endpoints", action="store_true", help="Show most requested endpoints")
    parser.add_argument("--limit", type=int, default=5, help="Number of top results to show")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    if args.limit <= 0:
        print("Error: --limit must be greater than 0", file=sys.stderr)
        sys.exit(1)

    try:
        records = parse_log_file(args.filename)
    except FileNotFoundError:
        print(f"Error: file not found: {args.filename}", file=sys.stderr)
        sys.exit(1)

    limit = args.limit

    show_all = not any([
        args.top_ips,
        args.top_codes,
        args.failed,
        args.top_endpoints
    ])

    results = {}
    if args.top_ips or show_all:
        results["top_ips"] = top_ips(records, limit)

    if args.top_codes or show_all:
        results["top_codes"] = top_codes(records, limit)

    if args.failed or show_all:
        results["failed_requests"] = failed_requests(records)

    if args.top_endpoints or show_all:
        results["top_endpoints"] = most_requested(records, limit)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if "top_ips" in results:
            print(results["top_ips"])

        if "top_codes" in results:
            print(results["top_codes"])

        if "failed_requests" in results:
            for line in results["failed_requests"]:
                print(line)

        if "top_endpoints" in results:
            print(results["top_endpoints"])

if __name__ == "__main__":
    main()