from fix_rspec_links.check import check_links

def test_check_links():
    orig_uri = "https://www.securecoding.cert.org/confluence/x/7gB9CQ"
    expected_redirect = "https://wiki.sei.cmu.edu/confluence/pages/tinyurl.action?urlIdentifier=7gB9CQ"
    checked = check_links([orig_uri])
    assert [res for res in checked] == [(orig_uri, expected_redirect, 404)]