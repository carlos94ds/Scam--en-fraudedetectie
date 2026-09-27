"""
Handmatig onderhouden lijst van bekende, betrouwbare domeinen (banken,
overheid, grote NL- en internationale diensten).

Het ML-model beoordeelt alleen kenmerken van de URL-tekst zelf (lengte,
cijfers, tekens, ...) en heeft geen besef van de reputatie van een domein.
Daardoor kan een heel gewone, wat langere pagina-URL van bijvoorbeeld een
bank of overheidsdienst (zoals "/particulier/inloggen") al snel als
verdacht worden beoordeeld, puur omdat legitieme URL's in de trainingsdata
meestal kort en kaal zijn. Voor domeinen in deze lijst slaan we het model
over en geven we altijd "laag risico".
"""

TRUSTED_DOMAINS = {
    # Banken
    "rabobank.nl", "ing.nl", "abnamro.nl", "asnbank.nl", "snsbank.nl",
    "triodos.nl", "bunq.com", "revolut.com", "knab.nl",
    # Overheid
    "overheid.nl", "belastingdienst.nl", "rijksoverheid.nl", "digid.nl",
    "mijnoverheid.nl", "politie.nl", "rdw.nl", "uwv.nl", "svb.nl",
    "kvk.nl", "dus-i.nl",
    # Grote NL-diensten
    "bol.com", "postnl.nl", "dhl.nl", "coolblue.nl", "ah.nl",
    # Grote internationale diensten
    "google.com", "microsoft.com", "apple.com", "amazon.com",
    "linkedin.com", "paypal.com", "wikipedia.org",
}


def is_trusted_domain(domain: str) -> bool:
    """True als domain gelijk is aan, of een subdomein van, een vertrouwd
    domein. "rabobank.nl.evil.com" matcht dus NIET op "rabobank.nl"."""
    domain = domain.lower().strip()
    if domain.startswith("www."):
        domain = domain[4:]
    return any(
        domain == trusted or domain.endswith("." + trusted)
        for trusted in TRUSTED_DOMAINS
    )
