from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VendorRule:
    slug: str
    directory_name: str
    match_terms: tuple[str, ...] = ()
    pdf_prefix: str = ""
    leistungsinhalt: str | None = None


VENDOR_RULES: dict[str, VendorRule] = {
    "aws": VendorRule(
        slug="aws",
        directory_name="AWS",
        match_terms=("amazon web services", "aws emea"),
        leistungsinhalt="Cloud-Infrastruktur / IT-Betrieb",
    ),
    "domainfactory": VendorRule(
        slug="domainfactory",
        directory_name="DomainFactory",
        match_terms=("domainfactory gmbh",),
        leistungsinhalt="Webhosting und Internet-Infrastruktur",
    ),
    "hosting": VendorRule(
        slug="hosting",
        directory_name="hosting.de",
        match_terms=("hosting.de gmbh",),
        leistungsinhalt="Domains, Hosting und technische Internet-Infrastruktur",
    ),
    "hp": VendorRule(
        slug="hp",
        directory_name="HP Instant Ink",
        match_terms=("hp inc instant ink de",),
        leistungsinhalt="Drucker-Abo und laufende Druckkosten",
    ),
    "moritz": VendorRule(
        slug="moritz",
        directory_name="Moritz",
        match_terms=("moritz hoeppner",),
        leistungsinhalt="Fremdleistung Softwareentwicklung",
    ),
    "google": VendorRule(
        slug="google",
        directory_name="Google",
        match_terms=("google cloud emea limited", "apps commerce"),
        leistungsinhalt="IT-/Cloud-Dienste von Google",
    ),
    "github": VendorRule(
        slug="github",
        directory_name="GitHub",
        match_terms=("github, inc.",),
        pdf_prefix="github-",
        leistungsinhalt="Quellcodeverwaltung und Entwicklerplattform",
    ),
}


def get_vendor_rule(vendor_slug: str) -> VendorRule:
    normalized_slug = vendor_slug.strip().lower()

    try:
        return VENDOR_RULES[normalized_slug]
    except KeyError as exc:
        supported = ", ".join(sorted(VENDOR_RULES))
        raise ValueError(
            f"Unbekannter Rechnungssteller: {vendor_slug}. Unterstützt: {supported}"
        ) from exc


def list_vendor_rules() -> tuple[VendorRule, ...]:
    return tuple(VENDOR_RULES[slug] for slug in sorted(VENDOR_RULES))


def list_expected_documents_export_dirs() -> tuple[str, ...]:
    vendor_dirs = [rule.directory_name for rule in list_vendor_rules()]
    vendor_dirs.append("PayPal")
    return tuple(vendor_dirs)


