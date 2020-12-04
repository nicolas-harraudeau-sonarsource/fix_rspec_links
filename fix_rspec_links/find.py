from collections import namedtuple
from typing import List, Generator
from urllib.parse import quote_plus
from copy import deepcopy

import click
from bs4 import BeautifulSoup
import requests

def find_new_cert_link(uri: str, texts: List[str]):
    """Find a new link corresponding to a CERT broken link."""
    if not texts:
        raise ValueError("CERT links require a text to be fixed. No text is provided.")
    if texts[0].startswith("CERT, "):
        cert_id = texts[0][len("CERT, "):]
    elif texts[0].startswith("CERT "):
        cert_id = texts[0][len("CERT "):]
    else:
        cert_id = texts[0]
    parser = "html.parser"
    cert_query = quote_plus(cert_id)
    search_page = requests.get(f"https://wiki.sei.cmu.edu/confluence/dosearchsite.action?queryString={cert_query}")
    parsed_search = BeautifulSoup(search_page.text, parser)
    result_links = parsed_search.findAll("a", {"class": "search-result-link"})
    long_link = None
    for link in result_links:
        if cert_id in link["href"]:
            long_link = link
            break
    if not long_link:
        return None
    
    new_page = requests.get(f"https://wiki.sei.cmu.edu{long_link['href']}")
    parsed_page = BeautifulSoup(new_page.text, parser)
    info_link = parsed_page.find(id="view-page-info-link")

    info_page = requests.get(f"https://wiki.sei.cmu.edu{info_link['href']}")
    parsed_info = BeautifulSoup(info_page.text, parser)
    tiny_link_text = parsed_info.find(text="Tiny Link: ")
    tiny_link = tiny_link_text.parent.next_sibling.next_sibling.findChild()["href"]

    return tiny_link



def find_new_uri(uri: str, texts: List[str]):
    """Find a new link corresponding to a broken link."""
    if uri.startswith("https://www.securecoding.cert.org/confluence/x"):
        return find_new_cert_link(uri, texts)
    return None


def find_new_links(links):
    """Find new links corresponding to broken links."""
    output = deepcopy(links)
    for uri, metadata in output.items():
        click.echo(f'New link for "{uri}" => ', nl=False, err=True)
        new_uri = find_new_uri(uri, metadata["texts"])
        if new_uri:
            output[uri]["new_link"] = new_uri
        else:
            output[uri]["new_link"] = None          
        click.echo(str(output[uri]["new_link"]), err=True)
    return output