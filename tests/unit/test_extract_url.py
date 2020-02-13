import sys, os
sys.path.append(os.path.realpath('oe_find_sds'))

import re
import pytest
from oe_find_sds.find_sds import extract_download_url_from_fisher, \
                                    extract_download_url_from_chemicalsafety, \
                                    extract_download_url_from_fluorochem


def mock_raise_exception():
    # return pytest.raises(RuntimeError)
    raise RuntimeError()


@pytest.mark.parametrize(
    "cas_nr, expect", [
        ('623-51-8', (
            'Fisher',
            'https://www.fishersci.com/store/msds?partNumber=AAA1432136&productDescription=ethyl-mercaptoacetate-&vendorId=VN00024248&keyword=true&countryCode=US&language=en'
            )
        ),
        ('28697-53-2', (
            'Fisher',
            'https://www.fishersci.com/store/msds?partNumber=S25650&productDescription=darabinose&vendorId=VN00115888&keyword=true&countryCode=US&language=en'
            )
        ),
        ('1450-76-6', (
            None,
            None
            )
        ),
        ('00000-00-0', (
            None,
            None
            )
        ),
    ]
)
def test_extract_url_from_fisher(cas_nr, expect):
    source, url = extract_download_url_from_fisher(cas_nr) or (None, None)
    assert (source, url) == expect


@pytest.mark.parametrize(
    "cas_nr, expect", [
        ('623-51-8', None)
    ]
)
def test_extract_url_from_fisher_with_exception(monkeypatch, cas_nr, expect):
    monkeypatch.setattr('oe_find_sds.find_sds.requests.get', mock_raise_exception)
    result = extract_download_url_from_fisher(cas_nr)
    assert result == expect


@pytest.mark.parametrize(
    "cas_nr, expect", [
        ('623-51-8', (
            'ChemicalSafety',
            'http://sds.chemicalsafety.com/sds/pda/msds/getpdf.ashx?action=msdsdocument&auth=200C200C200C200C2008207A200D2078200C200C200C200C200C200C200C200C200C2008&param1=ZmRwLjFfNzM2MzAwMDNORQ==&unique='
            )
        ),
        ('28697-53-2', (
            'ChemicalSafety',
            'http://sds.chemicalsafety.com/sds/pda/msds/getpdf.ashx?action=msdsdocument&auth=200C200C200C200C2008207A200D2078200C200C200C200C200C200C200C200C200C2008&param1=ZmRwLjFfMjQ3MDYyMDNORQ==&unique='
            )
        ),
        ('1450-76-6', (
            'ChemicalSafety',
            'http://sds.chemicalsafety.com/sds/pda/msds/getpdf.ashx?action=msdsdocument&auth=200C200C200C200C2008207A200D2078200C200C200C200C200C200C200C200C200C2008&param1=ZmRwLjFfNTI5ODU1MDNORQ==&unique='
            )
        ),
        ('00000-00-0', (
            None,
            None
            )
        ),
    ]
)
def test_extract_url_from_chemicalsafety(cas_nr, expect):
    source, url = extract_download_url_from_chemicalsafety(cas_nr) or (None, None)
    # Chemicalsafety return url with changing `...&unique=some-number`. 
    # Use regex to remove this number for consistent result
    url = re.sub(r'(?<=unique=)\d+$', '', url) if url else None
    assert (source, url) == expect


@pytest.mark.parametrize(
    "cas_nr, expect", [
        ('623-51-8', None)
    ]
)
def test_extract_url_from_chemicalsafety_with_exception(monkeypatch, cas_nr, expect):
    monkeypatch.setattr('oe_find_sds.find_sds.requests.post', mock_raise_exception)
    result = extract_download_url_from_chemicalsafety(cas_nr)
    assert result == expect


@pytest.mark.parametrize(
    "cas_nr, expect", [
        ('623-51-8', (
            None,
            None
            )
        ),
        ('28697-53-2', (
            'Fluorochem',
            'https://www.cheminfo.org/webservices/msds?brand=fluorochem&catalog=237868&embed=true'
            )
        ),
        ('1450-76-6', (
            'Fluorochem',
            'https://www.cheminfo.org/webservices/msds?brand=fluorochem&catalog=219286&embed=true'
            )
        ),
        ('00000-00-0', (
            None,
            None
            )
        ),
    ]
)
def test_extract_url_from_fluorochem(cas_nr, expect):
    source, url = extract_download_url_from_fluorochem(cas_nr) or (None, None)
    assert (source, url) == expect


@pytest.mark.parametrize(
    "cas_nr, expect", [
        ('28697-53-2', None)
    ]
)
def test_extract_url_from_fluorochem_with_exception(monkeypatch, cas_nr, expect):
    monkeypatch.setattr('oe_find_sds.find_sds.requests.post', mock_raise_exception)
    result = extract_download_url_from_fluorochem(cas_nr)
    assert result == expect
