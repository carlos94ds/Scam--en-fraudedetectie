"""
De 'brein'-logica van de applicatie, los van de Streamlit-UI. Dit maakt het
apart testbaar met pytest, zonder de webserver te hoeven starten.
"""
import os
import json
import joblib

from src.feature_extraction import extract_full_features
from src.train_production_model import FEATURE_ORDER

FEATURE_EXPLANATIONS = {
    "URLLength": ("Deze link is ongewoon lang.", "Deze link heeft een gewone lengte."),
    "DomainLength": ("De domeinnaam is ongewoon lang.", "De domeinnaam heeft een gewone lengte."),
    "IsDomainIP": ("De link gebruikt een kaal IP-adres in plaats van een domeinnaam.", "De link gebruikt een normale domeinnaam."),
    "TLDLength": ("Het laatste stukje van het domein is ongewoon lang.", "Het laatste stukje van het domein heeft een gewone lengte."),
    "NoOfSubDomain": ("De link heeft veel onderdelen voor de domeinnaam.", "De link heeft een eenvoudige domeinopbouw."),
    "HasObfuscation": ("De link bevat vreemde gecodeerde tekens.", "De link bevat geen vreemde gecodeerde tekens."),
    "NoOfObfuscatedChar": ("De link bevat meerdere vreemde gecodeerde tekens.", "De link bevat geen vreemde gecodeerde tekens."),
    "ObfuscationRatio": ("Een groot deel van de link bestaat uit gecodeerde tekens.", "De link bevat nauwelijks gecodeerde tekens."),
    "NoOfLettersInURL": ("De link bevat weinig gewone letters.", "De link bevat vooral gewone letters."),
    "LetterRatioInURL": ("De link bestaat voor een klein deel uit letters.", "De link bestaat grotendeels uit letters."),
    "NoOfDegitsInURL": ("De link bevat ongewoon veel cijfers.", "De link bevat weinig cijfers."),
    "DegitRatioInURL": ("Een groot deel van de link bestaat uit cijfers.", "De link bevat weinig cijfers."),
    "NoOfEqualsInURL": ("De link bevat veel is-gelijk-tekens.", "De link bevat weinig is-gelijk-tekens."),
    "NoOfQMarkInURL": ("De link bevat veel vraagtekens.", "De link bevat weinig vraagtekens."),
    "NoOfAmpersandInURL": ("De link bevat veel &-tekens.", "De link bevat weinig &-tekens."),
    "NoOfOtherSpecialCharsInURL": ("De link bevat veel ongewone tekens.", "De link bevat weinig ongewone tekens."),
    "SpacialCharRatioInURL": ("Een groot deel van de link bestaat uit ongewone tekens.", "De link bevat weinig ongewone tekens."),
    "IsHTTPS": ("Deze link gebruikt geen beveiligde verbinding (https).", "Deze link gebruikt een beveiligde verbinding (https)."),
    "CharContinuationRate": ("De opbouw van de link wisselt sterk tussen letters, cijfers en tekens.", "De link heeft een rustige, herkenbare opbouw."),
    "URLCharProb": ("De link bevat tekencombinaties die ongebruikelijk zijn.", "De link bevat gewone, herkenbare tekencombinaties."),
    "TLDLegitimateProb": ("Dit soort domeinextensie komt vaker voor bij nepwebsites.", "Dit soort domeinextensie komt vaker voor bij betrouwbare websites."),
}


def load_resources(model_dir):
    model = joblib.load(os.path.join(model_dir, "production_model.pkl"))
    scaler = joblib.load(os.path.join(model_dir, "production_scaler.pkl"))
    with open(os.path.join(model_dir, "tld_probability_table.json")) as f:
        tld_data = json.load(f)
    with open(os.path.join(model_dir, "char_frequency_table.json")) as f:
        char_data = json.load(f)
    return model, scaler, tld_data, char_data


def classify_risk(p_phishing: float) -> str:
    """Zet een phishing-kans om in een van drie risiconiveaus.

    Grenzen (0,2 / 0,6) zijn een eerste, beargumenteerde keuze: onder 20%
    kans laag risico, boven 60% kans hoog risico, daartussen "mogelijk".
    """
    if p_phishing < 0.2:
        return "laag"
    if p_phishing < 0.6:
        return "mogelijk"
    return "hoog"


def explain(model, feature_values_scaled, feature_names, top_n=3):
    contributions = model.coef_[0] * feature_values_scaled
    order = sorted(range(len(feature_names)), key=lambda i: abs(contributions[i]), reverse=True)
    reasons = []
    for i in order[:top_n]:
        name = feature_names[i]
        pushes_to_phishing = contributions[i] < 0
        pair = FEATURE_EXPLANATIONS.get(name)
        if pair:
            reasons.append(pair[0] if pushes_to_phishing else pair[1])
    return reasons


def analyse_url(url, model, scaler, tld_data, char_data, feature_order=FEATURE_ORDER):
    features = extract_full_features(
        url,
        tld_prob_table=tld_data["table"],
        char_freq_table=char_data["table"],
        default_tld_prob=tld_data["default"],
        default_char_prob=char_data["default"],
    )
    X = [[features[name] for name in feature_order]]
    X_scaled = scaler.transform(X)
    proba = model.predict_proba(X_scaled)[0]
    p_phishing = proba[0]
    risk = classify_risk(p_phishing)
    reasons = explain(model, X_scaled[0], feature_order)
    return risk, reasons, p_phishing
