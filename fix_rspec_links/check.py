"""Check that links are valid."""

from collections import namedtuple

import click
import requests

CheckedLink = namedtuple("Link", ["origin_uri", "redirect_uri", "status_code"])

def check_links(uris):
    for uri in uris:
        click.echo(f"Checking {uri} ", nl=False)
        result = requests.head(uri, allow_redirects=True)
        click.echo(result.status_code)
        yield CheckedLink(uri, result.url, result.status_code)
