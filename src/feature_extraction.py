"""
Eigen, zelfstandige berekening van de 22 URL-only kenmerken uit een ruwe
URL-string. We gebruiken dit zowel om het model opnieuw te trainen als om
straks in de webapplicatie een door de gebruiker ingevoerde URL te
analyseren, zodat trainen en live gebruik altijd consistent zijn.
"""
import re
from urllib.parse import urlparse

SPECIAL_CHARS_ALLOWED = set("/:.-_")  # tekens die we niet als "bijzonder" tellen
IP_PATTERN = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


def _char_class(ch):
    if ch.isalpha():
        return "letter"
    if ch.isdigit():
        return "digit"
    return "other"


def extract_base_features(url: str) -> dict:
    """Berekent de kenmerken die puur uit de tekst van de URL zelf volgen."""
    url = url.strip()
    parsed = urlparse(url if "://" in url else f"http://{url}")
    domain = parsed.netloc.split(":")[0]  # poortnummer eraf, indien aanwezig
    domain_parts = domain.split(".") if domain else []

    is_ip = 1 if IP_PATTERN.match(domain) else 0

    if is_ip or len(domain_parts) <= 1:
        tld = ""
        n_subdomains = 0
    else:
        tld = domain_parts[-1]
        # aantal subdomeinen = aantal onderdelen min domeinnaam en TLD
        n_subdomains = max(0, len(domain_parts) - 2)

    n_letters = sum(c.isalpha() for c in url)
    n_digits = sum(c.isdigit() for c in url)
    n_obfuscated = url.count("%")
    n_special = sum(
        1 for c in url if not c.isalnum() and c not in SPECIAL_CHARS_ALLOWED
    )

    length = len(url) if len(url) > 0 else 1  # deling door 0 voorkomen

    # CharContinuationRate: hoe vaak een teken hetzelfde "soort" is (letter/
    # cijfer/overig) als het teken ervoor. Een lage waarde betekent veel
    # afwisseling tussen letters, cijfers en symbolen, wat vaker voorkomt bij
    # samengeflanste phishing-URL's.
    if len(url) > 1:
        continuations = sum(
            1 for i in range(1, len(url)) if _char_class(url[i]) == _char_class(url[i - 1])
        )
        char_continuation_rate = continuations / (len(url) - 1)
    else:
        char_continuation_rate = 1.0

    return {
        "URLLength": len(url),
        "DomainLength": len(domain),
        "IsDomainIP": is_ip,
        "TLD": tld,
        "TLDLength": len(tld),
        "NoOfSubDomain": n_subdomains,
        "HasObfuscation": 1 if n_obfuscated > 0 else 0,
        "NoOfObfuscatedChar": n_obfuscated,
        "ObfuscationRatio": n_obfuscated / length,
        "NoOfLettersInURL": n_letters,
        "LetterRatioInURL": n_letters / length,
        "NoOfDegitsInURL": n_digits,
        "DegitRatioInURL": n_digits / length,
        "NoOfEqualsInURL": url.count("="),
        "NoOfQMarkInURL": url.count("?"),
        "NoOfAmpersandInURL": url.count("&"),
        "NoOfOtherSpecialCharsInURL": n_special,
        "SpacialCharRatioInURL": n_special / length,
        "IsHTTPS": 1 if parsed.scheme == "https" else 0,
        "CharContinuationRate": char_continuation_rate,
    }


def char_probability(url: str, char_freq_table: dict, default_prob: float) -> float:
    """Gemiddelde 'hoe gewoon is dit teken' score, op basis van een vooraf
    berekende frequentietabel uit onze eigen trainingsdata."""
    if len(url) == 0:
        return default_prob
    probs = [char_freq_table.get(c, default_prob) for c in url]
    return sum(probs) / len(probs)


def tld_legitimate_probability(tld: str, tld_prob_table: dict, default_prob: float) -> float:
    """Hoe vaak komt deze TLD voor bij legitieme URL's in onze trainingsdata."""
    return tld_prob_table.get(tld, default_prob)


def extract_full_features(url: str, tld_prob_table: dict, char_freq_table: dict,
                            default_tld_prob: float, default_char_prob: float) -> dict:
    """Alle 22 URL-only kenmerken samen, klaar om in het model te stoppen."""
    features = extract_base_features(url)
    features["URLCharProb"] = char_probability(url, char_freq_table, default_char_prob)
    features["TLDLegitimateProb"] = tld_legitimate_probability(
        features["TLD"], tld_prob_table, default_tld_prob
    )
    return features
