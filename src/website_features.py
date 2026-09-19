"""
Live ophalen en analyseren van de opgegeven website zelf (fase 2 van het
project — de MVP deed alleen de URL-tekst).

Twee verantwoordelijkheden staan hier los van elkaar:
1. fetch_website(): haalt de pagina veilig op (SSRF-bescherming, timeout,
   maximale downloadgrootte).
2. compute_website_features(): berekent uit de opgehaalde HTML dezelfde
   soort kenmerken als de WEBSITE_FEATURES-kolommen in de PhiUSIIL-dataset,
   zodat model B (getraind in src/train_url_website_model.py) hier live
   kenmerken krijgt die aansluiten bij waarmee hij getraind is.

Belangrijk: dit bezoekt een door de gebruiker opgegeven URL vanaf de
server. Dat is precies het aanvalsoppervlak van SSRF (Server-Side Request
Forgery) — een kwaadwillende gebruiker zou een interne URL kunnen invoeren
(bijv. een cloud-metadata-endpoint of een interne server) om de server dat
te laten bezoeken. fetch_website() blokkeert daarom alle IP's die niet
"gewoon publiek" zijn, voordat er verbinding wordt gemaakt.
"""
import ipaddress
import re
import socket
from difflib import SequenceMatcher
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

MAX_DOWNLOAD_BYTES = 2 * 1024 * 1024  # 2 MB: genoeg voor de meeste HTML, voorkomt geheugenmisbruik
REQUEST_TIMEOUT = 6  # seconden, connect + read gecombineerd via 'timeout='
MAX_REDIRECTS = 5
USER_AGENT = "VerdachtLink/1.0 (+educatief project; analyseert alleen structuur, geen inhoud)"

SOCIAL_DOMAINS = (
    "facebook.com", "instagram.com", "twitter.com", "x.com", "linkedin.com",
    "youtube.com", "tiktok.com", "pinterest.com", "snapchat.com", "whatsapp.com",
)
BANK_KEYWORDS = ("bank", "ideal", "swift", "iban")
PAY_KEYWORDS = ("pay", "betaal", "checkout", "creditcard", "payment")
CRYPTO_KEYWORDS = ("crypto", "bitcoin", "ethereum", "wallet", "blockchain")


class WebsiteFetchError(Exception):
    """Kon de website niet veilig of succesvol ophalen (geblokkeerd, timeout, te groot, HTTP-fout, ...)."""


def _is_public_ip(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved or ip.is_unspecified:
        return False
    return True


def _assert_safe_host(hostname: str):
    """Zoekt alle IP-adressen op waar deze hostnaam naar wijst en weigert als
    er ook maar één niet-publiek adres bij zit (SSRF-bescherming). Dit is een
    best-effort check: een aanvaller met controle over DNS zou in theorie
    tussen de check en de echte request van adres kunnen wisselen
    (DNS-rebinding). Voor een schoolproject is dit een redelijke, uitlegbare
    verdediging; voor een productieomgeving zou je ook op verbindingsniveau
    willen pinnen op het gecontroleerde IP."""
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as e:
        raise WebsiteFetchError(f"Kon domein niet oplossen: {e}") from e

    ips = {info[4][0] for info in infos}
    if not ips:
        raise WebsiteFetchError("Geen IP-adressen gevonden voor dit domein.")
    for ip in ips:
        if not _is_public_ip(ip):
            raise WebsiteFetchError("Dit adres wijst naar een niet-openbaar netwerk en wordt niet bezocht.")


def fetch_website(url: str):
    """Haalt de pagina veilig op. Retourneert (html, final_url, n_redirects).
    Gooit WebsiteFetchError als het niet lukt of niet veilig is."""
    url = url.strip()
    if "://" not in url:
        url = f"http://{url}"

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise WebsiteFetchError("Alleen http(s)-links kunnen bezocht worden.")
    if not parsed.hostname:
        raise WebsiteFetchError("Geen geldige hostnaam in deze link.")

    current_url = url
    n_redirects = 0
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    for _ in range(MAX_REDIRECTS + 1):
        hostname = urlparse(current_url).hostname
        _assert_safe_host(hostname)

        try:
            response = session.get(
                current_url,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=False,
                stream=True,
            )
        except requests.RequestException as e:
            raise WebsiteFetchError(f"Kon de pagina niet ophalen: {e}") from e

        if response.is_redirect or response.is_permanent_redirect:
            location = response.headers.get("Location")
            response.close()
            if not location:
                raise WebsiteFetchError("Doorverwijzing zonder bestemming.")
            current_url = urljoin(current_url, location)
            n_redirects += 1
            if n_redirects > MAX_REDIRECTS:
                raise WebsiteFetchError("Te veel doorverwijzingen.")
            continue

        if response.status_code >= 400:
            response.close()
            raise WebsiteFetchError(f"Pagina gaf foutcode {response.status_code}.")

        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type and content_type != "":
            response.close()
            raise WebsiteFetchError("Dit is geen HTML-pagina.")

        chunks = []
        total = 0
        for chunk in response.iter_content(chunk_size=8192):
            total += len(chunk)
            if total > MAX_DOWNLOAD_BYTES:
                response.close()
                raise WebsiteFetchError("Pagina is te groot om te analyseren.")
            chunks.append(chunk)
        response.close()

        html = b"".join(chunks).decode(response.encoding or "utf-8", errors="replace")
        return html, current_url, n_redirects

    raise WebsiteFetchError("Te veel doorverwijzingen.")


def _title_match_score(text_a: str, text_b: str) -> float:
    """Ruwe gelijkenis (0-100) tussen twee stukken tekst, gebruikt om te zien
    of de paginatitel bij het domein/de URL past (phishingpagina's hebben
    vaak een titel die niets met het domein te maken heeft)."""
    if not text_a or not text_b:
        return 0.0
    return round(SequenceMatcher(None, text_a.lower(), text_b.lower()).ratio() * 100, 2)


def compute_website_features(html: str, original_url: str, final_url: str, n_redirects: int) -> dict:
    """Berekent de website-kenmerken uit de opgehaalde HTML. Namen en
    betekenis volgen zo dicht mogelijk de WEBSITE_FEATURES-kolommen uit
    src/feature_lists.py / de PhiUSIIL-dataset."""
    soup = BeautifulSoup(html, "html.parser")
    parsed_final = urlparse(final_url)
    domain = parsed_final.netloc.split(":")[0]

    lines = html.splitlines()
    line_of_code = len(lines)
    largest_line_length = max((len(line) for line in lines), default=0)

    title_tag = soup.find("title")
    title_text = title_tag.get_text(strip=True) if title_tag else ""
    has_title = 1 if title_text else 0

    favicon = soup.find("link", rel=lambda v: v and "icon" in v.lower())
    has_favicon = 1 if favicon else 0

    robots_tag = soup.find("meta", attrs={"name": lambda v: v and v.lower() == "robots"})
    robots_value = robots_tag.get("content", "").strip().lower() if robots_tag else "none"
    if not robots_value:
        robots_value = "none"

    viewport_tag = soup.find("meta", attrs={"name": lambda v: v and v.lower() == "viewport"})
    is_responsive = 1 if viewport_tag else 0

    description_tag = soup.find("meta", attrs={"name": lambda v: v and v.lower() == "description"})
    has_description = 1 if description_tag and description_tag.get("content", "").strip() else 0

    n_iframe = len(soup.find_all("iframe"))
    n_image = len(soup.find_all("img"))
    n_css = len(soup.find_all("link", rel=lambda v: v and "stylesheet" in v.lower())) + len(soup.find_all("style"))
    n_js = len(soup.find_all("script"))

    scripts_text = " ".join(tag.get_text() for tag in soup.find_all("script"))
    n_popup = len(re.findall(r"window\.open\s*\(", scripts_text))

    forms = soup.find_all("form")
    has_external_form_submit = 0
    for form in forms:
        action = form.get("action", "")
        if action and action.startswith(("http://", "https://")):
            action_domain = urlparse(action).netloc.split(":")[0]
            if action_domain and action_domain != domain:
                has_external_form_submit = 1
                break

    has_submit_button = 1 if soup.find(["button"], type="submit") or soup.find("input", type="submit") else 0
    has_hidden_fields = 1 if soup.find("input", type="hidden") else 0
    has_password_field = 1 if soup.find("input", type="password") else 0

    page_text_lower = soup.get_text(" ", strip=True).lower()
    has_social_net = 1 if any(sd in html.lower() for sd in SOCIAL_DOMAINS) else 0
    bank = 1 if any(kw in page_text_lower for kw in BANK_KEYWORDS) else 0
    pay = 1 if any(kw in page_text_lower for kw in PAY_KEYWORDS) else 0
    crypto = 1 if any(kw in page_text_lower for kw in CRYPTO_KEYWORDS) else 0
    has_copyright_info = 1 if ("©" in html or "copyright" in page_text_lower) else 0

    n_self_ref, n_empty_ref, n_external_ref = 0, 0, 0
    for a_tag in soup.find_all("a"):
        href = (a_tag.get("href") or "").strip()
        if href in ("", "#"):
            n_empty_ref += 1
            continue
        if href.startswith(("http://", "https://")):
            href_domain = urlparse(href).netloc.split(":")[0]
            if href_domain == domain:
                n_self_ref += 1
            else:
                n_external_ref += 1
        else:
            # relatieve link (/pagina, pagina.html, ...) telt als zelf-referentie
            n_self_ref += 1

    domain_title_match = _title_match_score(domain, title_text)
    url_title_match = _title_match_score(original_url, title_text)

    return {
        "LineOfCode": line_of_code,
        "LargestLineLength": largest_line_length,
        "HasTitle": has_title,
        "DomainTitleMatchScore": domain_title_match,
        "URLTitleMatchScore": url_title_match,
        "HasFavicon": has_favicon,
        "Robots": robots_value,
        "IsResponsive": is_responsive,
        "NoOfURLRedirect": n_redirects,
        "NoOfSelfRedirect": n_redirects if urlparse(original_url).netloc.split(":")[0] == domain else 0,
        "HasDescription": has_description,
        "NoOfPopup": n_popup,
        "NoOfiFrame": n_iframe,
        "HasExternalFormSubmit": has_external_form_submit,
        "HasSocialNet": has_social_net,
        "HasSubmitButton": has_submit_button,
        "HasHiddenFields": has_hidden_fields,
        "HasPasswordField": has_password_field,
        "Bank": bank,
        "Pay": pay,
        "Crypto": crypto,
        "HasCopyrightInfo": has_copyright_info,
        "NoOfImage": n_image,
        "NoOfCSS": n_css,
        "NoOfJS": n_js,
        "NoOfSelfRef": n_self_ref,
        "NoOfEmptyRef": n_empty_ref,
        "NoOfExternalRef": n_external_ref,
    }


def encode_for_model_b(raw_features: dict, tld_vocab: list, robots_vocab: list, feature_columns: list):
    """Past dezelfde bucketing/one-hot-encoding toe als tijdens het trainen
    van model B (zie build_features() in src/train_url_website_model.py) en
    lijnt het resultaat uit op de exacte kolomvolgorde waarmee dat model is
    getraind (feature_columns, opgeslagen als url_website_feature_columns.pkl).
    Onbekende categorieën (een TLD of Robots-waarde die tijdens trainen niet
    voorkwam) vallen buiten alle dummy-kolommen — precies zoals bij trainen."""
    import pandas as pd

    row = dict(raw_features)
    tld = row.pop("TLD", "")
    robots = row.pop("Robots", "none")

    encoded = dict(row)
    tld_bucket = tld if tld in tld_vocab else "overig"
    for cat in tld_vocab + ["overig"]:
        encoded[f"TLD_{cat}"] = 1 if tld_bucket == cat else 0
    for cat in robots_vocab:
        encoded[f"Robots_{cat}"] = 1 if robots == cat else 0

    df = pd.DataFrame([encoded])
    df = df.reindex(columns=feature_columns, fill_value=0)
    return df
