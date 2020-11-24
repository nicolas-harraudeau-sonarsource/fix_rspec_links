from fix_rspec_links.fix import get_new_link

def test_get_new_cert_link():
    new_link = get_new_link(
        "https://www.securecoding.cert.org/confluence/x/7gB9CQ",
        ["CERT, DCL59-CPP."]
    )
    assert new_link == "https://wiki.sei.cmu.edu/confluence/display/cplusplus/DCL59-CPP.+Do+not+define+an+unnamed+namespace+in+a+header+file"
