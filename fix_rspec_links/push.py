import json

import click
import requests

def push_rspecs(host, auth, rspecs):
    """Push RSPECs to Jira"""
    for rspec in rspecs:
        description = rspec["fields"]["description"]
        click.echo(f"Pushing {rspec['key']} ", err=True)
        data = {
            "update": {
                "description": [
                    {
                        "set": description
                    }
                ],
            }
        }
        result = requests.put(
            f"{host}/rest/api/latest/issue/{rspec['key']}",
            json=data,
            auth=auth
        )
        result.raise_for_status()


