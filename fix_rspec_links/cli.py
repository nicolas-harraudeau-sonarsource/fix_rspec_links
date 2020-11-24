import json

import click
from requests.auth import HTTPBasicAuth
from fix_rspec_links.fetch import fetch_rspecs as _fetch_rspecs
from fix_rspec_links.extract import extract_links as _extract_links
from fix_rspec_links.fix import fix_links as _fix_links
from fix_rspec_links.check import check_links as _check_links
from fix_rspec_links.utils import serialize_sets_as_lists

#
# Jira API when this script was implemented: 7.13.11
# https://docs.atlassian.com/software/jira/docs/api/REST/7.13.11
#

@click.group()
def cli():
    pass


def get_host(environment):
    if environment == "dev":
        return "https://sonarsource-jira-test.valiantys.net/"
    else:
        raise NotImplementedError("Production environment is not supported yet.")

@cli.command()
@click.option("-u", "--username")
@click.option("--password", prompt=True, confirmation_prompt=False,
              hide_input=True)
@click.option("-e", "--environment", default="dev")
@click.option("--start", default=0)
@click.option("--end", default=1000)
@click.option("-o", "--output", default="rspecs.json", type=click.File(mode='w'))
def fetch_rspecs(username, password, environment, start, end, output):
    """Fetch RSPECs from Jira and dump them in a file."""
    rspecs = _fetch_rspecs(get_host(environment), HTTPBasicAuth(username, password), start, end)
    output.write(json.dumps(rspecs, sort_keys=True, indent=4))


@cli.command()
@click.option("-i", "--input", default="rspecs.json", type=click.File(mode='r'))
@click.option("-o", "--output", default="original_links.json", type=click.File(mode='w'))
def extract_links(input, output):
    """Read a file created by "fetch_rspecs", extract all links in it and dump the result in a file."""
    rspecs = json.load(input)
    links = _extract_links(rspecs)
    output.write(json.dumps(links, sort_keys=True, indent=4, default=serialize_sets_as_lists))



@cli.command()
@click.option("-i", "--input", default="original_links.json", type=click.File(mode='r'))
@click.option("-o", "--output", default="checked_links.json", type=click.File(mode='w'))
def check_links(input, output):
    """Read a file created by "extract_links", check all links validity and dump the result in a file."""
    orig_links = json.load(input)
    checked_links = _check_links(orig_links)
    # Reformat a bit the data
    result = {}
    for (orig_link, texts), (_, redirect, status_code) in zip(orig_links.items(), checked_links):
        result[orig_link] = {"texts": texts, "redirect": redirect, "status": status_code}
    output.write(json.dumps(result, sort_keys=True, indent=4))

# @cli.command()
# @click.option("-i", "--input", default="original_links.json", type=click.File(mode='r'))
# @click.option("-o", "--output", default="fixed_links.json", type=click.File(mode='w'))
# def fix_links(input, output):
#     """Read a file created by "fetch_rspecs", fix all links in it and dump the result in a file."""
#     rspecs = json.load(input)
#     links = extract_rspecs_links(rspecs)
#     output.write(json.dumps([uri for uri in links], sort_keys=True, indent=4))