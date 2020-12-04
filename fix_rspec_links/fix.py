from copy import deepcopy

from fix_rspec_links.extract import extract_rspec_links


def fix_rspecs(rspecs, new_links):
    """Fix rspecs by replacing broken links and return the new rspecs."""
    fixed_rspecs = []
    for rspec in rspecs:
        description = rspec["fields"]["description"]
        if not description:
            continue

        fixed = False
        for text, old_uri in extract_rspec_links(description):
            if old_uri in new_links:
                new_uri = new_links[old_uri]["new_link"]
                if new_uri:
                    description = description.replace(old_uri, new_uri)
                    fixed = True

        if fixed:
            new_rspec = deepcopy(rspec)
            new_rspec["fields"]["description"] = description
            fixed_rspecs.append(new_rspec)

    return fixed_rspecs
