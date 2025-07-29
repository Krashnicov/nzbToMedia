#!/usr/bin/env python3
"""Trigger post-processing via API for SABnzbd downloads.

This script is intended to be called by SABnzbd as a post-processing
script. It expects the path to the completed download as the first
command line argument.

The script calls the postprocess endpoint using the following
parameters:
- force_replace: true
- return_data: true
- process_method: move
- delete: true

Set the environment variable ``POSTPROCESS_URL`` to override the default
base URL (``http://localhost:8080``).
"""

import json
import os
import sys
import urllib.parse
import urllib.request

API_KEY = "a7d6b10fd3c974b0dc5035a3d838eb38"


def build_url(base_url: str, path: str) -> str:
    params = {
        "cmd": "postprocess",
        "path": path,
        "force_replace": 1,
        "return_data": 1,
        "process_method": "move",
        "delete": 1,
    }
    query = urllib.parse.urlencode(params)
    return f"{base_url.rstrip('/')}/api/{API_KEY}/?{query}"


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <path>", file=sys.stderr)
        return 1

    download_path = argv[1]
    base_url = os.environ.get("POSTPROCESS_URL", "http://localhost:8080")
    url = build_url(base_url, download_path)

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
    except Exception as exc:
        print(f"Failed to post-process: {exc}", file=sys.stderr)
        return 1

    if not data:
        return 0

    try:
        payload = json.loads(data.decode("utf-8"))
        print(json.dumps(payload, indent=2))
    except Exception:
        print(data.decode("utf-8"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
