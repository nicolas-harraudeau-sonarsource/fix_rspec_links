from collections import namedtuple
from typing import List, Generator
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
import requests

from fix_rspec_links.errors import UnfixableLink

def get_new_cert_link(uri: str, texts: List[str]):
    if not texts:
        raise ValueError("CERT links require a text to be fixed. No text is provided.")
    cert_query = quote_plus(texts[0])
    search_result = requests.get(f"https://wiki.sei.cmu.edu/confluence/dosearchsite.action?queryString={cert_query}")
    soup = BeautifulSoup(search_result.text, 'html.parser')
    result_links = soup.findAll("a", {"class": "search-result-link"})
    if not result_links:
        raise UnfixableLink(f'No alternative link found for [{texts[0]}|{uri}].')
    return f"https://wiki.sei.cmu.edu{result_links[0]['href']}"



def get_new_link(uri: str, texts: List[str]):
    if uri.startswith("https://www.securecoding.cert.org/confluence/x"):
        return get_new_cert_link(uri, texts)
    raise UnfixableLink(f"No function implemented to fix link {uri}")


def fix_links(links):
    fixed_links = {}
    for link in links:
        new_link = get_new_link(link)
        if new_link:
            fixed_links[link] = new_link
        else:
            fixed_links[link] = None          
    return fixed_links