#!/usr/bin/env python3
"""
Sample API runner for the Zoho Show REST API.

Shows the whole loop end to end: refresh an OAuth access token, call a couple of
read-only endpoints, and print the JSON the API returns.

This script talks to the API directly with `requests` so it runs against the
spec as published, with no generated SDK required. If you would rather use a
generated client, see "Generate an SDK" in the README - the auth flow below is
identical, you just hand the access token to the generated Configuration.

Setup
-----
1. Register a client at https://api-console.zoho.com (type: Self Client or
   Server-based) and note the Client ID and Client Secret.

2. Generate a refresh token for the scope this script needs:

       ZohoShow.showdocslist.READ

3. Export your credentials, and the data centre your account lives in:

       export SHOW_CLIENT_ID=...
       export SHOW_CLIENT_SECRET=...
       export SHOW_REFRESH_TOKEN=...
       export SHOW_DC=com            # com | in | eu | com.au | sa | ae | com.cn | jp | sg | uk | zohocloud.ca (Canada)

4. Install the one dependency and run:

       pip install requests
       python sample_api_runner.py
"""

import json
import os
import sys

import requests

DC = os.getenv("SHOW_DC", "com")
# Canada is the one data centre whose hosts are not <name>.zoho.<tld>.
if DC in ("ca", "zohocloud.ca"):
    ACCOUNTS_HOST = "https://accounts.zohocloud.ca"
    API_HOST = "https://show.zohocloud.ca"
else:
    ACCOUNTS_HOST = f"https://accounts.zoho.{DC}"
    API_HOST = f"https://show.zoho.{DC}"
BASE = f"{API_HOST}/api/v1"

TIMEOUT = 30


class ShowError(RuntimeError):
    """An error reported by the API, or a transport failure."""


def get_access_token():
    """Exchange the long-lived refresh token for a short-lived access token."""
    missing = [k for k in ("SHOW_CLIENT_ID", "SHOW_CLIENT_SECRET", "SHOW_REFRESH_TOKEN")
               if not os.getenv(k)]
    if missing:
        sys.exit(f"Set these environment variables first: {', '.join(missing)}")

    resp = requests.post(
        f"{ACCOUNTS_HOST}/oauth/v2/token",
        data={
            "grant_type": "refresh_token",
            "client_id": os.environ["SHOW_CLIENT_ID"],
            "client_secret": os.environ["SHOW_CLIENT_SECRET"],
            "refresh_token": os.environ["SHOW_REFRESH_TOKEN"],
        },
        timeout=TIMEOUT,
    )
    body = resp.json()
    if "access_token" not in body:
        raise ShowError(f"Token refresh failed: {body}")
    return body["access_token"]


def call(token, method, path, **kwargs):
    """Call one endpoint and return the decoded JSON body."""
    resp = requests.request(
        method,
        f"{BASE}{path}",
        headers={"Authorization": f"Zoho-oauthtoken {token}"},
        timeout=TIMEOUT,
        **kwargs,
    )
    try:
        body = resp.json()
    except ValueError:
        body = {"raw": resp.text}
    if not resp.ok:
        raise ShowError(f"{method} {path} -> HTTP {resp.status_code}: {body}")
    return body


def main():
    token = get_access_token()

    print("Workspace:")
    print(json.dumps(call(token, "GET", "/workspace"), indent=2))

    print("\nMy presentations (first 5):")
    print(json.dumps(call(token, "GET", "/presentation", params={"count": 5}), indent=2))


if __name__ == "__main__":
    try:
        main()
    except ShowError as exc:
        sys.exit(str(exc))
