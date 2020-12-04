"""Check that links are valid."""

from collections import namedtuple

import click
import requests
from requests.exceptions import ConnectionError, ReadTimeout

CheckedLink = namedtuple("Link", ["origin_uri", "redirect_uri", "status_code", "error"])

def check_links(uris):
    result = {}
    for uri in uris:
        click.echo(f"Checking {uri} ", nl=False)
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
            'Accept': '*/*',
        }
        try:
            # Note: In theory this should be a HEAD request instead of a GET, but
            # some websites such as OWASP will return 404 instead of 200 in this case.
            response = requests.get(uri.strip(), allow_redirects=True, timeout=3, headers=headers)
            click.echo(response.status_code)
            result[uri] = CheckedLink(uri, response.url, response.status_code, None)
        except (ConnectionError, ReadTimeout) as e:
            click.echo(f"Error {str(e)}")
            result[uri] = CheckedLink(uri, None, None, str(e))
    return result

def filter_failed_links(links):
    return {link: metadata for (link, metadata) in links.items()
        if (metadata["status"] and metadata["status"] != 200) or metadata["error"]}
