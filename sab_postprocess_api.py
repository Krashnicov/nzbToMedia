#!/usr/bin/env python
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
try:  # Python 3
    import urllib.parse as urlparse
    import urllib.request as urlrequest
except ImportError:  # Python 2
    import urllib as urlparse
    import urllib2 as urlrequest

API_KEY = os.environ.get("SAB_API_KEY", "a7d6b10fd3c974b0dc5035a3d838eb38")


def build_url(base_url, path):
    params = {
        "cmd": "postprocess",
        "path": path,
        "force_replace": 1,
        "return_data": 1,
        "process_method": "move",
        "delete": 1,
    }
    query = urlparse.urlencode(params)
    base = base_url.rstrip('/')
    return "%s/api/%s/?%s" % (base, API_KEY, query)


def main(argv):
    if len(argv) < 2:
        print("Usage: %s <path>" % argv[0], file=sys.stderr)
        return 1

    download_path = argv[1]
    base_url = os.environ.get("POSTPROCESS_URL", "http://localhost:8080")
    url = build_url(base_url, download_path)

    try:
        response = urlrequest.urlopen(url)
        try:
            data = response.read()
        finally:
            response.close()
    except Exception as exc:
        print("Failed to post-process: %s" % exc, file=sys.stderr)
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
    exit(main(sys.argv))
