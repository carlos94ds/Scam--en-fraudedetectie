"""
Tests voor app/logic.py: de risico-indeling en de end-to-end analyse van een
URL, met het echte getrainde model.
"""
import os
import pytest

from app.logic import classify_risk, load_resources, analyse_url

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
