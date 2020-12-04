from collections import namedtuple
from typing import Final, Generator
import re

Link = namedtuple("Link", ["text", "uri"])

URL_PATTERN: Final = re.compile("\[([^[|]+)\|[ ]*(https?://[^\]]+)\]")

def extract_rspec_links(description: str) -> Generator[Link, None, None]:
    """Extract links from an RSPEC."""
    for match in URL_PATTERN.finditer(description):
        yield Link(match.group(1), match.group(2))


def extract_links(rspecs):
    """Extract links from RSPECs."""
    result = {}
    for rspec in rspecs:
        description = rspec["fields"]["description"]
        if not description:
            continue
        links = extract_rspec_links(description)
        for link in links:
            link_texts = result.setdefault(link.uri, set())
            link_texts.add(link.text)

    return result

                