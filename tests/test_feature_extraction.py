"""
Tests voor src/feature_extraction.py: controleren of de kenmerken kloppen
voor bekende, simpele voorbeelden, en of rare invoer niet crasht.
"""
from src.feature_extraction import extract_base_features, extract_urls_from_text


def test_url_length_klopt():
    features = extract_base_features("https://example.com")
    assert features["URLLength"] == len("https://example.com")


def test_https_wordt_herkend():
    https_features = extract_base_features("https://example.com")
    http_features = extract_base_features("http://example.com")
    assert https_features["IsHTTPS"] == 1
    assert http_features["IsHTTPS"] == 0


def test_ip_adres_wordt_herkend_als_domein():
    features = extract_base_features("http://192.168.1.1/login")
    assert features["IsDomainIP"] == 1


def test_gewoon_domein_is_geen_ip():
    features = extract_base_features("https://www.windesheim.nl")
    assert features["IsDomainIP"] == 0


def test_cijfers_worden_geteld():
    features = extract_base_features("https://voorbeeld123.nl")
    assert features["NoOfDegitsInURL"] == 3


def test_obfuscatie_wordt_herkend():
    features = extract_base_features("https://voorbeeld.nl/pad%20met%20codes")
    assert features["HasObfuscation"] == 1
    assert features["NoOfObfuscatedChar"] == 2


def test_geen_obfuscatie_bij_gewone_url():
    features = extract_base_features("https://voorbeeld.nl/gewoon-pad")
    assert features["HasObfuscation"] == 0


def test_lege_url_crasht_niet():
    # Belangrijk: een lege of ongeldige URL mag nooit een fout geven,
    # want een gebruiker kan per ongeluk op "Controleer" drukken zonder
    # geldige invoer.
    features = extract_base_features("")
    assert features["URLLength"] == 0
    assert features["LetterRatioInURL"] == 0


def test_subdomeinen_worden_geteld():
    features = extract_base_features("https://mail.voorbeeld.co.uk")
    assert features["NoOfSubDomain"] >= 1


def test_extract_urls_uit_bericht():
    tekst = "Uw pakket kon niet worden bezorgd. Bevestig via voorbeeld-bezorgdienst.tk/verify123"
    urls = extract_urls_from_text(tekst)
    assert len(urls) == 1
    assert "voorbeeld-bezorgdienst.tk" in urls[0]


def test_extract_urls_geen_link_gevonden():
    urls = extract_urls_from_text("Dit bericht bevat helemaal geen link.")
    assert urls == []


def test_extract_urls_meerdere_links_en_geen_duplicaten():
    tekst = "Kijk op https://a-voorbeeld.nl en ook op https://A-Voorbeeld.nl nog een keer, en op https://b-voorbeeld.nl"
    urls = extract_urls_from_text(tekst)
    assert len(urls) == 2  # de twee schrijfwijzen van dezelfde link tellen als één
