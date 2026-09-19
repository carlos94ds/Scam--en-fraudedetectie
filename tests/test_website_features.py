"""
Tests voor src/website_features.py: de veilige fetcher (SSRF-bescherming),
het berekenen van website-kenmerken uit HTML, en de encodering naar model
B's kolommen. De netwerk-oproepen worden hier altijd gemockt, zodat de
tests niet afhankelijk zijn van een echte internetverbinding of een echte
(mogelijk wisselende) website.
"""
import socket

import pytest
import requests

from src.website_features import (
    WebsiteFetchError,
    _is_public_ip,
    _assert_safe_host,
    fetch_website,
    compute_website_features,
    encode_for_model_b,
    MAX_DOWNLOAD_BYTES,
)


# --------------------------------------------------------------------------
# _is_public_ip / _assert_safe_host: de kern van de SSRF-bescherming
# --------------------------------------------------------------------------

@pytest.mark.parametrize("ip", [
    "127.0.0.1",        # loopback
    "10.0.0.5",          # privé (RFC1918)
    "192.168.1.1",       # privé (RFC1918)
    "172.16.0.1",        # privé (RFC1918)
    "169.254.169.254",   # link-local / cloud-metadata-endpoint
    "0.0.0.0",            # unspecified
    "224.0.0.1",         # multicast
    "::1",                # IPv6 loopback
    "fe80::1",            # IPv6 link-local
])
def test_is_public_ip_blokkeert_niet_publieke_adressen(ip):
    assert _is_public_ip(ip) is False


@pytest.mark.parametrize("ip", ["8.8.8.8", "1.1.1.1", "93.184.216.34"])
def test_is_public_ip_staat_publieke_adressen_toe(ip):
    assert _is_public_ip(ip) is True


def test_is_public_ip_ongeldige_string_is_niet_publiek():
    assert _is_public_ip("dit-is-geen-ip-adres") is False


def test_assert_safe_host_blokkeert_prive_adres(monkeypatch):
    monkeypatch.setattr(
        socket, "getaddrinfo",
        lambda host, port: [(socket.AF_INET, None, None, "", ("192.168.1.1", 0))],
    )
    with pytest.raises(WebsiteFetchError):
        _assert_safe_host("interne-server.local")


def test_assert_safe_host_staat_publiek_adres_toe(monkeypatch):
    monkeypatch.setattr(
        socket, "getaddrinfo",
        lambda host, port: [(socket.AF_INET, None, None, "", ("93.184.216.34", 0))],
    )
    _assert_safe_host("example.com")  # geen exception


def test_assert_safe_host_blokkeert_als_een_van_meerdere_ips_prive_is(monkeypatch):
    # Een hostnaam kan naar meerdere IP's wijzen (bijv. IPv4 + IPv6, of
    # load-balancing) - als er ook maar één niet-publiek adres bij zit,
    # weigeren we het geheel.
    monkeypatch.setattr(
        socket, "getaddrinfo",
        lambda host, port: [
            (socket.AF_INET, None, None, "", ("93.184.216.34", 0)),
            (socket.AF_INET, None, None, "", ("127.0.0.1", 0)),
        ],
    )
    with pytest.raises(WebsiteFetchError):
        _assert_safe_host("gemengd.example.com")


def test_assert_safe_host_dns_fout_geeft_website_fetch_error(monkeypatch):
    def raise_gaierror(host, port):
        raise socket.gaierror("naam kon niet worden opgelost")

    monkeypatch.setattr(socket, "getaddrinfo", raise_gaierror)
    with pytest.raises(WebsiteFetchError):
        _assert_safe_host("bestaat-niet.invalid")


# --------------------------------------------------------------------------
# fetch_website: end-to-end, met gemockte DNS-resolutie en HTTP-requests
# --------------------------------------------------------------------------

class FakeResponse:
    def __init__(self, status_code=200, headers=None, body=b"", is_redirect=False,
                 is_permanent_redirect=False, encoding="utf-8"):
        self.status_code = status_code
        self.headers = headers or {}
        self._body = body
        self.is_redirect = is_redirect
        self.is_permanent_redirect = is_permanent_redirect
        self.encoding = encoding
        self.closed = False

    def iter_content(self, chunk_size=8192):
        for i in range(0, len(self._body), chunk_size):
            yield self._body[i:i + chunk_size]

    def close(self):
        self.closed = True


def _patch_public_dns(monkeypatch):
    monkeypatch.setattr(
        socket, "getaddrinfo",
        lambda host, port: [(socket.AF_INET, None, None, "", ("93.184.216.34", 0))],
    )


def test_fetch_website_weigert_niet_http_schema():
    with pytest.raises(WebsiteFetchError):
        fetch_website("ftp://example.com/bestand")


def test_fetch_website_weigert_url_zonder_hostnaam():
    with pytest.raises(WebsiteFetchError):
        fetch_website("http:///pad-zonder-host")


def test_fetch_website_blokkeert_voordat_er_geconnect_wordt(monkeypatch):
    # Simuleert een SSRF-poging: de hostnaam lost op naar een intern adres.
    # De request mag dan nooit daadwerkelijk verstuurd worden.
    monkeypatch.setattr(
        socket, "getaddrinfo",
        lambda host, port: [(socket.AF_INET, None, None, "", ("127.0.0.1", 0))],
    )

    def fail_if_called(*args, **kwargs):
        raise AssertionError("requests.Session.get had niet aangeroepen mogen worden")

    monkeypatch.setattr(requests.Session, "get", fail_if_called)

    with pytest.raises(WebsiteFetchError):
        fetch_website("http://interne-dienst.local/")


def test_fetch_website_succesvol(monkeypatch):
    _patch_public_dns(monkeypatch)
    html = "<html><head><title>Voorbeeld</title></head><body>hoi</body></html>".encode("utf-8")
    response = FakeResponse(status_code=200, headers={"Content-Type": "text/html"}, body=html)
    monkeypatch.setattr(requests.Session, "get", lambda self, *a, **k: response)

    result_html, final_url, n_redirects = fetch_website("http://example.com")
    assert "Voorbeeld" in result_html
    assert final_url == "http://example.com"
    assert n_redirects == 0
    assert response.closed


def test_fetch_website_volgt_redirect_en_blokkeert_prive_bestemming(monkeypatch):
    calls = {"n": 0}

    def fake_getaddrinfo(host, port):
        calls["n"] += 1
        if calls["n"] == 1:
            return [(socket.AF_INET, None, None, "", ("93.184.216.34", 0))]
        return [(socket.AF_INET, None, None, "", ("169.254.169.254", 0))]

    monkeypatch.setattr(socket, "getaddrinfo", fake_getaddrinfo)

    redirect_response = FakeResponse(
        status_code=302, headers={"Location": "http://intern.local/geheim"}, is_redirect=True,
    )
    monkeypatch.setattr(requests.Session, "get", lambda self, *a, **k: redirect_response)

    with pytest.raises(WebsiteFetchError):
        fetch_website("http://example.com/start")


def test_fetch_website_weigert_te_grote_pagina(monkeypatch):
    _patch_public_dns(monkeypatch)
    te_groot = b"x" * (MAX_DOWNLOAD_BYTES + 1)
    response = FakeResponse(status_code=200, headers={"Content-Type": "text/html"}, body=te_groot)
    monkeypatch.setattr(requests.Session, "get", lambda self, *a, **k: response)

    with pytest.raises(WebsiteFetchError):
        fetch_website("http://example.com")


def test_fetch_website_weigert_niet_html_content(monkeypatch):
    _patch_public_dns(monkeypatch)
    response = FakeResponse(
        status_code=200, headers={"Content-Type": "application/pdf"}, body=b"%PDF-1.4",
    )
    monkeypatch.setattr(requests.Session, "get", lambda self, *a, **k: response)

    with pytest.raises(WebsiteFetchError):
        fetch_website("http://example.com/bestand.pdf")


def test_fetch_website_weigert_foutcode(monkeypatch):
    _patch_public_dns(monkeypatch)
    response = FakeResponse(status_code=404, headers={"Content-Type": "text/html"}, body=b"")
    monkeypatch.setattr(requests.Session, "get", lambda self, *a, **k: response)

    with pytest.raises(WebsiteFetchError):
        fetch_website("http://example.com/bestaat-niet")


# --------------------------------------------------------------------------
# compute_website_features: pure functie op HTML, geen netwerk nodig
# --------------------------------------------------------------------------

def test_compute_website_features_herkent_wachtwoordveld():
    html = '<html><body><form><input type="password"></form></body></html>'
    features = compute_website_features(html, "http://voorbeeld.nl", "http://voorbeeld.nl", 0)
    assert features["HasPasswordField"] == 1


def test_compute_website_features_geen_wachtwoordveld():
    html = "<html><body><p>Gewone pagina, geen formulier.</p></body></html>"
    features = compute_website_features(html, "http://voorbeeld.nl", "http://voorbeeld.nl", 0)
    assert features["HasPasswordField"] == 0


def test_compute_website_features_titel_matcht_domein():
    html = "<html><head><title>Voorbeeld Bedrijf</title></head><body></body></html>"
    features = compute_website_features(
        html, "http://voorbeeld-bedrijf.nl", "http://voorbeeld-bedrijf.nl", 0,
    )
    assert features["HasTitle"] == 1
    # De titel lijkt sterk op de domeinnaam, dus een relatief hoge score.
    assert features["DomainTitleMatchScore"] > 40


def test_compute_website_features_titel_matcht_niet_bij_phishing():
    html = "<html><head><title>Gratis cadeaubonnen winnen!!!</title></head><body></body></html>"
    features = compute_website_features(
        html, "http://mijn-bank-veilig-login.tk", "http://mijn-bank-veilig-login.tk", 0,
    )
    assert features["DomainTitleMatchScore"] < 40


def test_compute_website_features_geen_titel():
    html = "<html><head></head><body>Geen titel hier.</body></html>"
    features = compute_website_features(html, "http://voorbeeld.nl", "http://voorbeeld.nl", 0)
    assert features["HasTitle"] == 0


def test_compute_website_features_externe_form_submit():
    html = '<html><body><form action="http://ander-domein.tk/vangst"><input type="password"></form></body></html>'
    features = compute_website_features(html, "http://voorbeeld.nl", "http://voorbeeld.nl", 0)
    assert features["HasExternalFormSubmit"] == 1


def test_compute_website_features_telt_iframes_en_afbeeldingen():
    html = """
    <html><body>
        <iframe src="http://ergens.nl"></iframe>
        <img src="a.png"><img src="b.png"><img src="c.png">
    </body></html>
    """
    features = compute_website_features(html, "http://voorbeeld.nl", "http://voorbeeld.nl", 0)
    assert features["NoOfiFrame"] == 1
    assert features["NoOfImage"] == 3


def test_compute_website_features_bank_en_crypto_keywords():
    html = "<html><body>Log in bij je bank-account of betaal met bitcoin wallet.</body></html>"
    features = compute_website_features(html, "http://voorbeeld.nl", "http://voorbeeld.nl", 0)
    assert features["Bank"] == 1
    assert features["Crypto"] == 1


def test_compute_website_features_zonder_die_woorden():
    html = "<html><body>Dit is een gewone informatiepagina over katten.</body></html>"
    features = compute_website_features(html, "http://voorbeeld.nl", "http://voorbeeld.nl", 0)
    assert features["Bank"] == 0
    assert features["Pay"] == 0
    assert features["Crypto"] == 0


def test_compute_website_features_lege_en_externe_links():
    html = """
    <html><body>
        <a href="#">leeg</a>
        <a href="/pagina">zelf</a>
        <a href="http://voorbeeld.nl/pagina2">zelf, volledig</a>
        <a href="http://ander-domein.nl">extern</a>
    </body></html>
    """
    features = compute_website_features(html, "http://voorbeeld.nl", "http://voorbeeld.nl", 0)
    assert features["NoOfEmptyRef"] == 1
    assert features["NoOfSelfRef"] == 2
    assert features["NoOfExternalRef"] == 1


# --------------------------------------------------------------------------
# encode_for_model_b: kolommen moeten exact aansluiten op het getrainde model
# --------------------------------------------------------------------------

def test_encode_for_model_b_bekende_tld_en_robots():
    raw = {"TLD": "nl", "Robots": "index", "HasPasswordField": 1}
    tld_vocab = ["nl", "com"]
    robots_vocab = ["index", "noindex"]
    feature_columns = ["HasPasswordField", "TLD_nl", "TLD_com", "TLD_overig", "Robots_index", "Robots_noindex"]

    df = encode_for_model_b(raw, tld_vocab, robots_vocab, feature_columns)

    assert list(df.columns) == feature_columns
    assert df.loc[0, "TLD_nl"] == 1
    assert df.loc[0, "TLD_com"] == 0
    assert df.loc[0, "TLD_overig"] == 0
    assert df.loc[0, "Robots_index"] == 1
    assert df.loc[0, "Robots_noindex"] == 0
    assert df.loc[0, "HasPasswordField"] == 1


def test_encode_for_model_b_onbekende_tld_valt_in_overig():
    raw = {"TLD": "xyz", "Robots": "none"}
    tld_vocab = ["nl", "com"]
    robots_vocab = ["index", "noindex"]
    feature_columns = ["TLD_nl", "TLD_com", "TLD_overig", "Robots_index", "Robots_noindex"]

    df = encode_for_model_b(raw, tld_vocab, robots_vocab, feature_columns)

    assert df.loc[0, "TLD_overig"] == 1
    assert df.loc[0, "TLD_nl"] == 0
    assert df.loc[0, "TLD_com"] == 0
    # 'none' is geen bekende Robots-categorie in deze vocab: geen van de
    # Robots-kolommen wordt gezet, precies zoals bij trainen.
    assert df.loc[0, "Robots_index"] == 0
    assert df.loc[0, "Robots_noindex"] == 0


def test_encode_for_model_b_lijnt_altijd_uit_op_feature_columns():
    # Ook als raw_features extra of andere sleutels bevat dan
    # feature_columns, moet het resultaat precies feature_columns als
    # kolommen hebben (reindex met fill_value=0), zodat het model nooit
    # een vorm-mismatch krijgt.
    raw = {"TLD": "nl", "Robots": "none", "IetsWatNietInModelZit": 999}
    df = encode_for_model_b(raw, ["nl"], [], ["HasPasswordField", "TLD_nl", "TLD_overig"])

    assert list(df.columns) == ["HasPasswordField", "TLD_nl", "TLD_overig"]
    assert df.loc[0, "HasPasswordField"] == 0  # niet in raw_features -> fill_value=0
    assert df.loc[0, "TLD_nl"] == 1
