import json

import click
import requests

def fetch_rspecs(host, auth, start=0, end=100, page_size=100):
    """Fetch RSPECs from Jira"""
    rspecs = []
    for query_start in range(start, end, page_size):
        click.echo(f"Fetching RSPECS {query_start} -> {query_start + page_size}", err=True)
        query = {
            "jql": "project = RSPEC AND status in (Active, Deprecated, Superseded) ORDER BY created ASC",
            "startAt": query_start,
            "maxResults": page_size,
            "fields": [
                "summary",
                "description",
                "updated"
            ]
        }
        result = requests.post(
            f"{host}/rest/api/latest/search",
            json=query,
            auth=auth
        )
        result.raise_for_status()
        click.echo(f"Fetched {len(rspecs)} RSPECS", err=True)
        rspecs.extend(result.json()["issues"])
    return rspecs

