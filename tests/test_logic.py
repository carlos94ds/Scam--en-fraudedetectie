"""
Tests voor app/logic.py: de risico-indeling en de end-to-end analyse van een
URL, met het echte getrainde model.
"""
import os
import pytest

import app.logic as logic
from app.logic import (
    classify_risk,
    load_resources,
    analyse_url,
    website_resources_available,
    load_website_resources,
    analyse_url_and_website,
)
from src.website_features import WebsiteFetchError

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


def test_classify_risk_grenzen():
    assert classify_risk(0.0) == "laag"
    assert classify_risk(0.19) == "laag"
    assert classify_risk(0.2) == "mogelijk"
    assert classify_risk(0.59) == "mogelijk"
    assert classify_risk(0.6) == "hoog"
    assert classify_risk(1.0) == "hoog"


@pytest.fixture(scope="module")
def resources():
    if not os.path.exists(os.path.join(MODEL_DIR, "production_model.pkl")):
        pytest.skip("Productiemodel nog niet getraind (run src/train_production_model.py eerst).")
    return load_resources(MODEL_DIR)


def test_analyse_url_geeft_geldig_resultaat(resources):
    model, scaler, tld_data, char_data = resources
    risk, reasons, p_phishing = analyse_url(
        "https://www.voorbeeld-bedrijf.nl", model, scaler, tld_data, char_data
    )
    assert risk in {"laag", "mogelijk", "hoog"}
    assert 0.0 <= p_phishing <= 1.0
    assert len(reasons) <= 3


def test_analyse_url_geeft_altijd_uitleg(resources):
    model, scaler, tld_data, char_data = resources
    _, reasons, _ = analyse_url(
        "http://192.168.1.1/login%20nu%20snel?verify=1&x=2", model, scaler, tld_data, char_data
    )
    assert len(reasons) > 0


# --------------------------------------------------------------------------
# Model B (URL + website): analyse_url_and_website, met gemockte fetch_website
# zodat er geen echte website bezocht wordt tijdens het testen.
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def website_resources():
    if not website_resources_available(MODEL_DIR):
        pytest.skip("Model B nog niet getraind (run src/train_url_website_model.py eerst).")
    return load_website_resources(MODEL_DIR)


def _fake_website(html, final_url="http://voorbeeld.nl", n_redirects=0):
    """Vervangt fetch_website() door een functie die meteen de gegeven HTML
    teruggeeft, zonder netwerkverkeer."""
    def fake_fetch_website(url):
        return html, final_url, n_redirects
    return fake_fetch_website


def test_analyse_url_and_website_geeft_geldig_resultaat(monkeypatch, resources, website_resources):
    model, scaler, tld_data, char_data = resources
    model_b, scaler_b, feature_columns_b, vocab = website_resources

    html = "<html><head><title>Voorbeeld</title></head><body>Welkom</body></html>"
    monkeypatch.setattr(logic, "fetch_website", _fake_website(html, "http://voorbeeld.nl"))

    risk, reasons, p_phishing = analyse_url_and_website(
        "http://voorbeeld.nl", model_b, scaler_b, feature_columns_b, vocab, tld_data, char_data,
    )
    assert risk in {"laag", "mogelijk", "hoog"}
    assert 0.0 <= p_phishing <= 1.0
    assert len(reasons) <= 3


def test_analyse_url_and_website_werkt_in_alle_vertaalde_talen(monkeypatch, resources, website_resources):
    # Regressietest voor de fr/es/de/pt/it-uitbreiding van
    # FEATURE_EXPLANATIONS: een website-analyse mag in geen enkele taal een
    # KeyError geven, ook al zijn de top-features website-kenmerken.
    model, scaler, tld_data, char_data = resources
    model_b, scaler_b, feature_columns_b, vocab = website_resources

    html = (
        "<html><head><title>Verdachte pagina</title></head>"
        '<body><form action="http://ander-domein.tk"><input type="password"></form></body></html>'
    )
    monkeypatch.setattr(logic, "fetch_website", _fake_website(html, "http://verdacht-voorbeeld.tk"))

    for lang in ["nl", "en", "fr", "es", "de", "pt", "it"]:
        risk, reasons, _ = analyse_url_and_website(
            "http://verdacht-voorbeeld.tk", model_b, scaler_b, feature_columns_b, vocab,
            tld_data, char_data, lang=lang,
        )
        assert risk in {"laag", "mogelijk", "hoog"}


def test_analyse_url_and_website_geeft_website_fetch_error_door(monkeypatch, resources, website_resources):
    # De aanroeper (app/app.py) vangt WebsiteFetchError op om terug te vallen
    # op de URL-only-analyse; die exception moet dus ongewijzigd doorgegeven
    # worden, niet ingeslikt of vervangen door een andere fout.
    model, scaler, tld_data, char_data = resources
    model_b, scaler_b, feature_columns_b, vocab = website_resources

    def fake_fetch_website_faalt(url):
        raise WebsiteFetchError("kon niet bezocht worden")

    monkeypatch.setattr(logic, "fetch_website", fake_fetch_website_faalt)

    with pytest.raises(WebsiteFetchError):
        analyse_url_and_website(
            "http://onbereikbaar.tk", model_b, scaler_b, feature_columns_b, vocab, tld_data, char_data,
        )
